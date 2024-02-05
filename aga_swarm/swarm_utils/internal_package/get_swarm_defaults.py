from aga_swarm.swarm_utils.internal_package import get_json_data

def get_default_action_space_metadata() -> dict:
    return get_json_data('aga_swarm.actions', 'action_space_metadata.json')

def get_default_memory_space_metadata() -> dict: 
    return get_json_data('aga_swarm.memory', 'memory_space_metadata.json')