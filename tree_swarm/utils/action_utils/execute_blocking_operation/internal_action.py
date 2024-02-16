'''
This blocking operation will call the next_function_to_call of the node's action,
combining the args, context and swarm into the function call.

Think of this as the entrypoint back into the action after a blocking operation has been completed.
'''

from __future__ import annotations
from importlib import import_module
from typing import TYPE_CHECKING, Union

from tree_swarm.swarm.types import ActionSpace, SwarmState

if TYPE_CHECKING:
    from tree_swarm.swarm.types import Swarm, BlockingOperation, NodeOutput


def execute_blocking_operation(swarm: Swarm, blocking_operation: BlockingOperation) -> Union[BlockingOperation, NodeOutput]:
    action_space = ActionSpace(swarm=swarm)
    swarm_state = SwarmState(swarm=swarm)
    node_id = blocking_operation.node_id
    node = swarm_state[node_id]
    action_metadata = action_space[node.action_id]
    script_path = action_metadata.execution_metadata['script_path']
    action_script = import_module(script_path)
    
    combined_args = {}
    combined_args.update(blocking_operation.args)
    if blocking_operation.context is not None:
        combined_args.update(blocking_operation.context)
    
    return getattr(action_script, blocking_operation.next_function_to_call)(**combined_args)
