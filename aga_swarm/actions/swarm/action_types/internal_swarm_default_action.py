import importlib
from pydantic import validate_arguments

from aga_swarm.core.swarm.types import SwarmID
from aga_swarm.core.swarm.swarm_utils import get_default_action_space_metadata

@validate_arguments
def internal_swarm_default_action(action_type: str, swarm_id: SwarmID, params: dict):
    action_space_metadata = get_default_action_space_metadata()
    # Import dependencies
    dependencies = action_space_metadata[action_type]['dependencies']
    for package in dependencies:
        importlib.import_module(package)
    
    # Get config parameters required for this action
    required_configs = action_space_metadata[action_type]['configs']
    for config in required_configs: 
        try:
            params[config] = swarm_id['configs'][config]
        except KeyError:
            raise KeyError(f"Config {config} not found in swarm configs")
    
    # Import the main function from the path specified by the action_id
    action_type = action_type.replace('/', '.')
    if action_type.endswith('.py'):
        action_type = action_type[:-3]
    action = __import__(action_type, fromlist=[''])
    if hasattr(action, 'main'):
        main_function = getattr(action, 'main')
    else:
        raise AttributeError("No main function found in the script")
    
    return main_function(**params)

@validate_arguments
def main(action_id: str, swarm_id: SwarmID, params: dict):
    return internal_swarm_default_action(action_id, swarm_id, params)
