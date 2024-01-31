from pydantic import validate_call
import json
from pathlib import Path
from typing import Any, Dict, Union

from aga_swarm.swarm.types import SwarmID, Platform, SwarmState, SwarmHistory
from aga_swarm.utils.internal_swarm_utils import get_default_action_space_metadata, get_default_memory_space_metadata
from aga_swarm.utils.swarm_utils import make_folder, upload_file, retrieve_file

@validate_call
def setup_swarm_blueprint(blueprint_name: str, openai_key: str, frontend_url: str, platform: Platform, root_path: str) -> SwarmID:
    '''
        Setup a new blank swarm blueprint on your platform of choice.
        
        Parameters:
            - blueprint_name (str)
            - openai_key (str)
            - frontend_url (str): 
                The URL for the frontend interface of the swarm.
            - platform (str): 
                Choose between: 
                ['mac', 'windows', 'linux', 'azure', 'gcp', 'aws']
            - root_path (str): 
                The root path for this swarm blueprint and it's 
                instances to be stored. This should be an empty
                folder.
        
    '''
    paths = _build_swarm_paths(root_path, blueprint_name)
    swarm_id = SwarmID(
        instance_path=paths["instance_path"],
        root_path=root_path,
        platform=platform,
        action_space_metadata_path=paths["action_space_metadata_path"],
        memory_space_metadata_path=paths["memory_space_metadata_path"],
        stage_path=paths["stage_path"],
        state_path=paths["state_path"],
        history_path=paths["history_path"],
        configs={
            'openai_key': openai_key,
            'frontend_url': frontend_url
        }
    )
    _setup_swarm_space(swarm_id, 
        json.dumps(get_default_action_space_metadata()).encode('utf-8'), 
        json.dumps(get_default_memory_space_metadata()).encode('utf-8'))
    
    return swarm_id

@validate_call
def create_swarm_instance(blueprint_id: Union[SwarmID, Dict[str, Any]], instance_name: str) -> SwarmID:
    '''
    Create a new instance of a swarm blueprint.
    
    Parameters:
        - blueprint_id (SwarmID, dict): 
            The ID of the blueprint you want to create an instance of. You can also pass in the dictionary representation of a SwarmID.
        - instance_name (str): 
            The name of the instance you want to create.
    '''
    if isinstance(blueprint_id, dict):
        blueprint_id = SwarmID.model_validate(blueprint_id)
        
    paths = _build_swarm_paths(blueprint_id.root_path, instance_name)
    swarm_id = SwarmID(
        instance_path=paths["instance_path"],
        root_path=blueprint_id.root_path,
        platform=blueprint_id.platform,
        action_space_metadata_path=paths["action_space_metadata_path"],
        memory_space_metadata_path=paths["memory_space_metadata_path"],
        stage_path=paths["stage_path"],
        state_path=paths["state_path"],
        history_path=paths["history_path"],
        configs=blueprint_id.configs
    )
    action_space_metadata = retrieve_file(swarm_id, blueprint_id.action_space_metadata_path)
    memory_space_metadata = retrieve_file(swarm_id, blueprint_id.memory_space_metadata_path)
    _setup_swarm_space(swarm_id, action_space_metadata, memory_space_metadata)
    
    return swarm_id


'''
    Private functions
'''    

def _setup_swarm_space(swarm_id: SwarmID, action_space: bytes, memory_space: bytes) -> None:
    '''
        The "swarm space" is just the folder on your local machine 
        or blob storage used to your swarm blueprint and instances.
        
        All we are doing here is setting up the default swarm space
        in your chosen platform and folder.
    '''
    make_folder(swarm_id, f"{swarm_id.instance_path}/stage")
    upload_file(swarm_id, f"{swarm_id.instance_path}/action_space_metadata.json", action_space)
    upload_file(swarm_id, f"{swarm_id.instance_path}/memory_space_metadata.json", memory_space)
    upload_file(swarm_id, f"{swarm_id.instance_path}/state.json", SwarmState(nodes={}).model_dump_json().encode('utf-8'))
    upload_file(swarm_id, f"{swarm_id.instance_path}/history.json", SwarmHistory(frames=[]).model_dump_json().encode('utf-8'))
    upload_file(swarm_id, f"{swarm_id.instance_path}/swarm_id.json", swarm_id.model_dump_json().encode('utf-8'))


def _build_swarm_paths(root_path: str, instance_name: str) -> Dict[str, Path]:
    instance_path = Path(root_path, instance_name)
    return {
        "instance_path": str(instance_path),
        "action_space_metadata_path": str(instance_path / 'action_space_metadata.json'),
        "memory_space_metadata_path": str(instance_path / 'memory_space_metadata.json'),
        "stage_path": str(instance_path / 'stage'),
        "state_path": str(instance_path / 'state.json'),
        "history_path": str(instance_path / 'history.json')
    }