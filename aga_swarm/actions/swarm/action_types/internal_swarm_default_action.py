import importlib
import sys
from pydantic import validate_arguments

@validate_arguments
def internal_swarm_default_action(action_type: str, swarm: dict, params: dict):
    # Import dependencies
    dependencies = swarm['action_space'][action_type]['dependencies']
    for package in dependencies:
        importlib.import_module(package)
    
    # Get config parameters required for this action
    required_configs = swarm['action_space'][action_type]['configs']
    for config in required_configs: 
        try:
            params[config] = swarm['configs'][config]
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
def main(action_id: str, swarm: dict, params: dict):
    return internal_swarm_default_action(action_id, swarm, params)
