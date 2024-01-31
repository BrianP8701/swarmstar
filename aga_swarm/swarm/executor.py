from typing import Any, Dict

from aga_swarm.swarm.types import *
from aga_swarm.utils.swarm_utils import get_action_space_metadata
from aga_swarm.utils.internal_swarm_utils import import_internal_python_action

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
    
    if action_metadata.type == 'folder':
        raise ValueError(f"This action id {action_id} is a folder. You cannot execute a folder.")
    
    action_langauge = action_metadata.language
    action_is_internal = action_metadata.internal
    
    if action_is_internal:
        if action_langauge == 'python':
            return execute_internal_python_action(action_id, params)
        else:
            raise ValueError(f"This action language {action_langauge} is not supported.")
    else:
        # TODO implement support for non-internal actions
        raise ValueError(f"This action id {action_id} is not internal. I didn't implement handling for this yet.")


def execute_internal_python_action(action_metadata: ActionMetadata, params: Dict[str, Any]) -> Dict[str, Any]:
    '''
    Execute an internal python action.

    Parameters:
        - action_metadata (ActionMetadata): 
            The metadata of the action you want to execute.
        - swarm_id (SwarmID): 
            The ID of the swarm you want to execute the action in.
        - params (dict): 
            The parameters you want to pass to the action.

    Returns:
        - dict: 
            The result of the action.
    '''
    expected_params = action_metadata.input_schema
    for param_name, param_metadata in expected_params.items():
        if param_name not in params:
            raise ValueError(f"Missing parameter {param_name} when calling {action_metadata.name}.")
        if param_metadata.enum is not None:
            if params[param_name] not in param_metadata.enum:
                raise ValueError(f"Invalid value {params[param_name]} for parameter {param_name} for action {action_metadata.name}.")
        if param_metadata.type != type(params[param_name]):
            raise ValueError(f"Invalid type: {type(params[param_name])}, for parameter: {param_name}, for action: {action_metadata.name}. Expected: {param_metadata.type}.")
    action = import_internal_python_action(action_metadata.script_path)
    return action(**params)
