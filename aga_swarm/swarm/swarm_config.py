from pydantic import validate_call
import json
import os

from aga_swarm.swarm.types import SwarmID, Platform, SwarmState, SwarmHistory
from aga_swarm.utils.internal_swarm_utils import get_default_action_space_metadata, get_default_memory_space_metadata
from aga_swarm.actions.swarm.actions.action_types.internal_default_swarm_action import internal_default_swarm_action 

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
    swarm_id = SwarmID(
        instance_path=os.path.join(root_path, blueprint_name),
        root_path=root_path,
        platform=platform,
        action_space_metadata_path=os.path.join(root_path, blueprint_name, 'action_space_metadata.json'),
        memory_space_metadata_path=os.path.join(root_path, blueprint_name, 'memory_space_metadata.json'),
        stage_path=os.path.join(root_path, blueprint_name, 'stage'),
        state_path=os.path.join(root_path, blueprint_name, 'state'),
        history_path=os.path.join(root_path, blueprint_name, 'history'),
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
def create_swarm_instance(blueprint_id: SwarmID, instance_name: str) -> SwarmID:
    '''
    Create a new instance of a swarm blueprint.
    
    Parameters:
        - blueprint_id (SwarmID): 
            The ID of the blueprint you want to create an instance of.
        - instance_name (str): 
            The name of the instance you want to create.
    '''
    swarm_id = SwarmID(
        instance_path=os.path.join(blueprint_id.root_path, instance_name),
        root_path=blueprint_id.root_path,
        platform=blueprint_id.platform,
        action_space_metadata_path=os.path.join(blueprint_id.root_path, instance_name, 'action_space_metadata.json'),
        memory_space_metadata_path=os.path.join(blueprint_id.root_path, instance_name, 'memory_space_metadata.json'),
        stage_path=os.path.join(blueprint_id.root_path, instance_name, 'stage.json'),
        state_path=os.path.join(blueprint_id.root_path, instance_name, 'state.json'),
        history_path=os.path.join(blueprint_id.root_path, instance_name, 'history.json'),
        configs=blueprint_id.configs
    )
    retrieve_file_action_id = 'aga_swarm/actions/data/file_operations/retrieve_file/retrieve_file.py'
    action_space_metadata = internal_default_swarm_action(action_id=retrieve_file_action_id, 
        params={'file_path': blueprint_id.action_space_metadata_path, "swarm_id": swarm_id})['data']
    memory_space_metadata = internal_default_swarm_action(action_id=retrieve_file_action_id, 
        params={'file_path': blueprint_id.memory_space_metadata_path, "swarm_id": swarm_id})['data']
    _setup_swarm_space(swarm_id, action_space_metadata, memory_space_metadata)
    
    return swarm_id


'''
    Private functions
'''    

@validate_call
def _make_folder(swarm_id: SwarmID, folder_path: str) -> None:
    make_folder_action_id = 'aga_swarm/actions/data/folder_operations/make_folder/make_folder.py'
    internal_default_swarm_action(action_id=make_folder_action_id, 
        params={'folder_path': folder_path, "swarm_id": swarm_id})

@validate_call
def _upload_file(swarm_id: SwarmID, file_path: str, data: bytes) -> None:
    upload_file_action_id = 'aga_swarm/actions/data/file_operations/upload_file/upload_file.py'
    internal_default_swarm_action(action_id=upload_file_action_id, 
        params={'file_path': file_path, "swarm_id": swarm_id, 'data': data})

@validate_call
def _setup_swarm_space(swarm_id: SwarmID, action_space: bytes, memory_space: bytes) -> None:
    '''
        The "swarm space" is just the folder on your local machine 
        or blob storage used to your swarm blueprint and instances.
        
        All we are doing here is setting up the default swarm space
        in your chosen platform and folder.
    '''
    _make_folder(swarm_id, f"{swarm_id.instance_path}/stage")
    _upload_file(swarm_id, f"{swarm_id.instance_path}/action_space_metadata.json", action_space)
    _upload_file(swarm_id, f"{swarm_id.instance_path}/memory_space_metadata.json", memory_space)
    _upload_file(swarm_id, f"{swarm_id.instance_path}/state.json", SwarmState(nodes={}).model_dump_json().encode('utf-8'))
    _upload_file(swarm_id, f"{swarm_id.instance_path}/history.json", SwarmHistory(frames=[]).model_dump_json().encode('utf-8'))
    _upload_file(swarm_id, f"{swarm_id.instance_path}/swarm_id.json", swarm_id.model_dump_json().encode('utf-8'))
