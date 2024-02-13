from typing import Any, Dict, Union
from importlib import import_module

from aga_swarm.swarm.types import Swarm, SwarmNode, NodeOutput, BlockingOperation, ActionSpace

def execute_blocking_operation(swarm: Swarm, blocking_operation: BlockingOperation) -> Union[NodeOutput, BlockingOperation]:
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
    
    blocking_operation_type_map = {
        'openai_instructor_completion': 'aga_swarm.utils.action_utils.execute_blocking_operation.openai_instructor_completion',
        'internal_action': 'aga_swarm.utils.action_utils.execute_blocking_operation.internal_action'
    }
    
    blocking_operation_type = blocking_operation.type
    
    if blocking_operation_type not in blocking_operation_type_map:
        raise ValueError(f"Blocking operation type: `{blocking_operation_type.type}` is not supported.")
    else:
        pass
    
    blocking_operation_type_module = import_module(blocking_operation_type_map[blocking_operation_type])
    
    return blocking_operation_type_module.execute_blocking_operation(swarm, blocking_operation)
