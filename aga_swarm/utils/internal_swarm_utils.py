'''
    This module contains utility functions for interacting with the swarm
    space inside the package. These functions are not meant to be used
    outside of the package. Instead look at aga_swarm/swarm/swarm_utils.py
'''

from pydantic import validate_call

from aga_swarm.utils.file_utils import get_json_data

@validate_call
def get_default_action_space_metadata() -> dict:
    return get_json_data('aga_swarm.actions', 'action_space_metadata.json')

@validate_call
def get_default_memory_space_metadata() -> dict: 
    return get_json_data('aga_swarm.memory', 'memory_space_metadata.json')
