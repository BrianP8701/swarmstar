from typing import Any, Dict, Union
from importlib import import_module

from tree_swarm.swarm.types import Swarm, SwarmNode, NodeOutput, BlockingOperation, ActionSpace

def execute_node_action(swarm: Swarm, swarm_node: SwarmNode) -> Union[NodeOutput, BlockingOperation]:
    '''
    Execute any action in the swarm.

    Parameters:
        - action_id (str): 
            The ID of the action you want to execute.
        - swarm (Swarm): 
            The ID of the swarm you want to execute the action in.
        - params (dict): 
            The parameters you want to pass to the action.

    Returns:
        - dict: 
            The result of the action.
    '''
    
    action_type_map = {
        'internal_python_main': 'tree_swarm.utils.action_utils.execute_action.internal_python_main',
    }
    
    action_id = swarm_node.action_id
    node_id = swarm_node.node_id
    message = swarm_node.message
    action_space = ActionSpace(swarm=swarm)
    action_metadata = action_space[action_id]
    action_type = action_metadata.type
    
    if action_type not in action_type_map:
        raise ValueError(f"Action type: `{action_type}` from action id: `{action_id}` is not supported yet.")
    action_type_module = import_module(action_type_map[action_type])
    
    return action_type_module.execute_action(swarm, action_metadata, node_id, message)
