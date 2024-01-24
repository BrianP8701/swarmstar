from pydantic import validate_arguments
from utils.file_utils import get_json_data

@validate_arguments
def get_default_action_tree() -> dict:
    return get_json_data('actions', 'action_space.json')

@validate_arguments
def get_default_memory_tree() -> dict: 
    return get_json_data('memory', 'memory_space.json')
