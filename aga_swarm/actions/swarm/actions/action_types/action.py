from pydantic import validate_call
from typing import Dict, Any

from aga_swarm.swarm.types import SwarmID
from aga_swarm.utils.swarm_utils import get_action_type

def action(action_id: str, params: Dict[str, Any], swarm_id: SwarmID) -> dict:
    """
        Passes the action to the appropriate action_type for execution.

        This function serves as a universal entry point for executing actions.

        Every action action_type is expected to follow the default_swarm_action.py
        action type.
    """
    action_type = get_action_type(swarm_id, action_id)
    
    # Import the main function from the path specified by the action_id
    action_type = action_type.replace('/', '.')
    if action_type.endswith('.py'):
        action_type = action_type[:-3]
    action = __import__(action_type, fromlist=[''])
    if hasattr(action, 'main'):
        main_function = getattr(action, 'main')
    else:
        raise AttributeError(f"No main function found in the script {action_id}")
    
    params.pop('action_type', None)
    return main_function(**{'action_id': action_id, 'params': params})

@validate_call
def main(action_id: str, params: Dict[str, Any], swarm_id: SwarmID):
    return action(action_id, params, swarm_id)
