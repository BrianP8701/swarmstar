from pydantic import validate_arguments
import json

from aga_swarm.utils.file_utils import get_json_data
from aga_swarm.actions.swarm.action_types.internal_python_script_call_main import internal_python_script_call_main as execute

@validate_arguments
def get_default_action_space() -> dict:
    return get_json_data('aga_swarm.actions', 'action_space.json')

@validate_arguments
def get_default_memory_space() -> dict: 
    return get_json_data('aga_swarm.memory', 'memory_space.json')

@validate_arguments
def setup_swarm_space(swarm_blueprint: dict) -> dict:
    execute(f'aga_swarm/actions/data/folder_operations/make_folder/make_folder.py', 
            swarm_blueprint, 
            {'folder_path': f"{swarm_blueprint['configs']['root_path']}/swarm_blueprint", "swarm": swarm_blueprint})

    swarm_blueprint_str = json.dumps(swarm_blueprint)
    swarm_blueprint_bytes = swarm_blueprint_str.encode('utf-8')
    execute(f'aga_swarm/actions/data/file_operations/file_upload/file_upload.py',
            swarm_blueprint,
            {'file_path': f"{swarm_blueprint['configs']['root_path']}/swarm_blueprint/swarm_blueprint.json",
            'data': swarm_blueprint_bytes, "swarm": swarm_blueprint})