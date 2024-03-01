"""
This blocking operation will call the next_function_to_call of the node's action,
combining the args, context and swarm into the function call.

Think of this as the entrypoint back into the action after a blocking operation has been completed.
"""

from __future__ import annotations

from importlib import import_module
from typing import TYPE_CHECKING, List, Union

from pydantic import BaseModel

from swarmstar.swarm.types import ActionSpace, SwarmState

if TYPE_CHECKING:
    from swarmstar.swarm.types import BlockingOperation, SwarmConfig, SwarmOperation


# This blocking operation doesn't have set args, it will just pass the args and context to the next function to call
class expected_args(BaseModel):
    any


def blocking(
    swarm: SwarmConfig, blocking_operation: BlockingOperation
) -> Union[SwarmOperation, List[SwarmOperation]]:
    action_space = ActionSpace(swarm=swarm)
    swarm_state = SwarmState(swarm=swarm)
    node_id = blocking_operation.node_id
    node = swarm_state[node_id]
    action_metadata = action_space[node.action_id]
    action_name = action_metadata.name
    script_path = action_metadata.internal_action_path
    action_file = import_module(script_path)
    combined_args = {}
    combined_args.update(blocking_operation.args)
    if blocking_operation.context is not None:
        combined_args.update(blocking_operation.context)

    action_class = getattr(action_file, action_name)
    action_instance = action_class(swarm=swarm, node=node)
    return getattr(action_instance, blocking_operation.next_function_to_call)(
        **combined_args
    )
