import importlib
import sys
from pydantic import validate_arguments

@validate_arguments
def internal_python_script_call_main(action_id: str, swarm: dict, params: dict):
    # Import dependencies
    dependencies = swarm['action_space'][action_id]['dependencies']
    for package in dependencies:
        importlib.import_module(package)
    
    # Get config parameters required for this action
    required_configs = swarm['action_space'][action_id]['configs']
    for config in required_configs: 
        try:
            params[config] = swarm['configs'][config]
        except KeyError:
            raise KeyError(f"Config {config} not found in swarm configs")
    
    # Import the main function from the path specified by the action_id
    action_id = action_id.replace('/', '.')
    if action_id.endswith('.py'):
        action_id = action_id[:-3]
    script = __import__(action_id, fromlist=[''])
    if hasattr(script, 'main'):
        main_function = getattr(script, 'main')
    else:
        raise AttributeError("No main function found in the script")
    
    # Install dependencies
    return main_function(**params)

@validate_arguments
def main(action_id: str, swarm: dict, params: dict):
    return internal_python_script_call_main(action_id, swarm, params)
