from typing import Union, List
from importlib import import_module

from swarm_star.swarm.types import SwarmConfig, SwarmNode, SwarmOperation, ExecuteOperation, ActionSpace, SwarmHistory

def execute_node_action(swarm: SwarmConfig, execute_operation: ExecuteOperation) -> SwarmOperation:
    action_type_map = {
        'internal_action': 'swarm_star.utils.swarm_utils.action_operations.internal_action',
    }
    node = execute_operation.node
    action_id = node.action_id
    node_id = node.node_id
    message = node.message
    action_space = ActionSpace(swarm=swarm)
    action_metadata = action_space[action_id]
    action_type = action_metadata.type
    
    if action_type not in action_type_map:
        raise ValueError(f"Action type: `{action_type}` from action id: `{action_id}` is not supported yet.")
    action_type_module = import_module(action_type_map[action_type])
    
    action_output = action_type_module.execute_action(swarm, action_metadata, node_id, message)
    swarm_history = SwarmHistory(swarm=swarm)
    swarm_history.add_event(execute_operation)
    
    return action_output