from pydantic import validate_arguments

from aga_swarm.utils.file_utils import get_json_data

@validate_arguments
def get_default_action_space_metadata() -> dict:
    return get_json_data('aga_swarm.actions', 'action_space_metadata.json')

@validate_arguments
def get_default_memory_space_metadata() -> dict: 
    return get_json_data('aga_swarm.memory', 'memory_space_metadata.json')