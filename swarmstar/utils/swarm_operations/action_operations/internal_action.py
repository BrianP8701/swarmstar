from importlib import import_module
from typing import List, Union

from swarmstar.types import SwarmConfig, SwarmOperation, ActionOperation
from swarmstar.utils.swarmstar_space import (
    get_swarm_node, 
    get_action_metadata,
)

def execute_action(swarm_config: SwarmConfig, action_operation: ActionOperation) -> Union[SwarmOperation, List[SwarmOperation]]:
    """
    This handles actions that are internal to swarmstar.
    """
    node_id = action_operation.node_id
    node = get_swarm_node(swarm_config, node_id)
    action_metadata = get_action_metadata(swarm_config, node.action_id)
    
    internal_action_path = action_metadata.internal_action_path
    action_class = getattr(import_module(internal_action_path), "Action")
    action_instance = action_class(swarm_config=swarm_config, node_id=node_id)
    
    function_to_call = action_operation.function_to_call
    args = action_operation.args
    return getattr(action_instance, function_to_call)(**args)
