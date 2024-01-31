'''
    Functions for getting default stuff from the swarm.
'''

from pydantic import validate_call

from aga_swarm.utils.internal_file_utils import get_json_data

@validate_call
def get_default_action_space_metadata() -> dict:
    return get_json_data('aga_swarm.actions', 'action_space_metadata.json')

@validate_call
def get_default_memory_space_metadata() -> dict: 
    return get_json_data('aga_swarm.memory', 'memory_space_metadata.json')
