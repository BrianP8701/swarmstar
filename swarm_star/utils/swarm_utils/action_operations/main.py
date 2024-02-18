from typing import Union, List
from importlib import import_module

from swarm_star.swarm.types import SwarmConfig, SwarmState, SwarmOperation, ExecuteOperation, ActionSpace, SwarmHistory

def execute_node_action(swarm: SwarmConfig, execute_operation: ExecuteOperation) -> SwarmOperation:
    action_type_map = {
        'internal_action': 'swarm_star.utils.swarm_utils.action_operations.internal_action',
    }
    swarm_state = SwarmState(swarm=swarm)
    node_id = execute_operation.node_id
    node = swarm_state[node_id]
    action_id = node.action_id
    message = node.message
    action_space = ActionSpace(swarm=swarm)
    action_metadata = action_space[action_id]
    action_type = action_metadata.type
    
    if action_type not in action_type_map:
        raise ValueError(f"Action type: `{action_type}` from action id: `{action_id}` is not supported yet.")
    action_type_module = import_module(action_type_map[action_type])
    
    action_output = action_type_module.execute_action(swarm, node, action_metadata)
    swarm_history = SwarmHistory(swarm=swarm)
    swarm_history.add_event(execute_operation)
    
    return action_output