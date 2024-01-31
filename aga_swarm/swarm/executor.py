from typing import Any, Dict
from importlib import import_module

from aga_swarm.swarm.types import *
from aga_swarm.utils.swarm_utils import get_action_space_metadata

def dynamic_import_main_function(module_name):
    module = import_module(module_name)
    main = getattr(module, 'main', None)  
    if main is None:
        raise AttributeError(f"No main function found in the script {module_name}")
    return main

def execute_action(action_id: str, swarm_id: SwarmID, params: Dict[str, Any]) -> Dict[str, Any]:
    '''
    Execute an action in the swarm.

    Parameters:
        - action_id (str): 
            The ID of the action you want to execute.
        - swarm_id (SwarmID): 
            The ID of the swarm you want to execute the action in.
        - params (dict): 
            The parameters you want to pass to the action.

    Returns:
        - dict: 
            The result of the action.
    '''
    action_space_metadata = get_action_space_metadata(swarm_id)
    action_metadata = action_space_metadata.get(action_id)
    if action_metadata is None:
        raise ValueError(f"This action id {action_id} does not exist.")
    
    action_langauge = action_metadata['language']
    
    if action_langauge == 'python':
        return execute_python_action(action_id, swarm_id, params)
    
    raise ValueError(f"This action language {action_langauge} is not supported.")

def execute_python_action(action_id: str, swarm_id: SwarmID, params: Dict[str, Any]) -> Dict[str, Any]:
    action = dynamic_import_main_function(action_id)
    return action(swarm_id=swarm_id, params=params)
