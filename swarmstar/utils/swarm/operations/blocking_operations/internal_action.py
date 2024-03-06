"""
This blocking operation will call the next_function_to_call of the node's action,
combining the args, context and swarm into the function call.

Think of this as the entrypoint back into the action after a blocking operation has been completed.
"""

from importlib import import_module
from typing import List, Union

from pydantic import BaseModel

from swarmstar.swarm.types import BlockingOperation, SwarmConfig, SwarmOperation
from swarmstar.utils.swarm.swarmstar_space import get_swarm_node, get_action_metadata

# This blocking operation doesn't have set args, it will just pass the args and context to the next function to call
class expected_args(BaseModel):
    any


def blocking(
    swarm_config: SwarmConfig, blocking_operation: BlockingOperation
) -> Union[SwarmOperation, List[SwarmOperation]]:
    node_id = blocking_operation.node_id
    node = get_swarm_node(swarm_config, node_id)
    action_metadata = get_action_metadata(swarm_config, node.action_id)
    action_name = action_metadata.name
    script_path = action_metadata.internal_action_path
    action_file = import_module(script_path)
    combined_args = {}
    combined_args.update(blocking_operation.args)
    if blocking_operation.context is not None:
        combined_args.update(blocking_operation.context)

    action_class = getattr(action_file, action_name)
    action_instance = action_class(swarm=swarm_config, node=node)
    return getattr(action_instance, blocking_operation.next_function_to_call)(
        **combined_args
    )
