from pydantic import validate_arguments, Dict, Any

from aga_swarm.swarm.types import SwarmID, ActionSpaceMetadata
from aga_swarm.swarm.swarm_utils import get_action_space_metadata

def default_swarm_action(action_id: str, params: Dict[str, Any], swarm_id: SwarmID) -> dict:
    '''        
        This action calls the main function of the action script specified by the action_id with the params provided.
    '''
    action_space_metadata: ActionSpaceMetadata = get_action_space_metadata()
    
    # Get config parameters required for this action
    required_configs = action_space_metadata[action_id].required_configs
    for config in required_configs: 
        try:
            if getattr(swarm_id.configs, config) is None:
                raise KeyError
            params[config] = getattr(swarm_id.configs, config)
        except KeyError:
            raise KeyError(f"Config {config} not found in swarm configs or value is None")
    
    # Import the main function from the path specified by the action_id
    import_action_id = action_id.replace('/', '.')
    if import_action_id.endswith('.py'):
        import_action_id = import_action_id[:-3]
    action = __import__(import_action_id, fromlist=[''])
    if hasattr(action, 'main'):
        main_function = getattr(action, 'main')
    else:
        raise AttributeError("No main function found in the script")
    
    return main_function(**params)

@validate_arguments
def main(action_id: str, params: Dict[str, Any], swarm_id: SwarmID):
    return default_swarm_action(action_id, params, swarm_id)
