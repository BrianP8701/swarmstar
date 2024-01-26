from pydantic import validate_arguments
from utils.file_utils import get_json_data
from actions.swarm.action_types.internal_python_script_call_main import internal_python_script_call_main

@validate_arguments
def get_default_action_space() -> dict:
    return get_json_data('actions', 'action_space.json')

@validate_arguments
def get_default_memory_space() -> dict: 
    return get_json_data('memory', 'memory_space.json')

@validate_arguments
def setup_swarm_space(swarm_blueprint: dict) -> dict:
    internal_python_script_call_main('actions/data/folder_operations/make_folder/mac_make_folder.py', 
                                     swarm_blueprint, 
                                     {'folder_path': f"{swarm_blueprint['configs']['root_path']}/swarm_blueprint"})
