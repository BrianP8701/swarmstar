from pydantic import validate_arguments
import json
import os

from aga_swarm.swarm.types import SwarmID
from aga_swarm.swarm.internal_swarm_utils import get_default_action_space_metadata, get_default_memory_space_metadata
from aga_swarm.actions.swarm.action_types.internal_swarm_default_action import internal_swarm_default_action as execute

@validate_arguments
def setup_swarm_blueprint(blueprint_name: str, openai_key: str, frontend_url: str, platform: str, root_path: str) -> SwarmID:
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

@validate_arguments
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
    
    # Get action and memory space from blueprint
    retrieve_file_action_id = 'aga_swarm/actions/data/file_operations/retrieve_file/retrieve_file.py'
    action_space_metadata = execute(retrieve_file_action_id, swarm_id, 
        {'file_path': blueprint_id.action_space_metadata_path, "swarm_id": swarm_id})['data']
    memory_space_metadata = execute(retrieve_file_action_id, swarm_id, 
        {'file_path': blueprint_id.memory_space_metadata_path, "swarm_id": swarm_id})['data']
    
    _setup_swarm_space(swarm_id, action_space_metadata, memory_space_metadata)
    
    return swarm_id


'''
    Private functions
'''    

@validate_arguments
def _setup_swarm_space(swarm_id: SwarmID, action_space: bytes, memory_space: bytes) -> None:
    '''
        The "swarm space" is just the folder on your local machine 
        or blob storage used to your swarm blueprint and instances.
    '''
    make_folder_action_id = 'aga_swarm/actions/data/folder_operations/make_folder/make_folder.py'
    upload_file_action_id = 'aga_swarm/actions/data/file_operations/upload_file/upload_file.py'
    
    # Create swarm instance folder
    execute(make_folder_action_id, swarm_id, 
            {'folder_path': swarm_id.instance_path, "swarm_id": swarm_id})
    # Create stage
    execute(make_folder_action_id, swarm_id, 
            {'folder_path': f"{swarm_id.instance_path}/stage", "swarm_id": swarm_id})
    # Create action space metadata
    execute(upload_file_action_id, swarm_id, 
            {'file_path': f"{swarm_id.instance_path}/action_space_metadata.json", "swarm_id": swarm_id,
            'data': action_space})
    # Create memory space metadata
    execute(upload_file_action_id, swarm_id, 
            {'file_path': f"{swarm_id.instance_path}/memory_space_metadata.json", "swarm_id": swarm_id,
            'data': memory_space})
    # Create state
    execute(upload_file_action_id, swarm_id, 
        {'file_path': f"{swarm_id.instance_path}/state.json", "swarm_id": swarm_id,
        'data': json.dumps({}).encode('utf-8')})
    # Create history
    execute(upload_file_action_id, swarm_id, 
        {'file_path': f"{swarm_id.instance_path}/history.json", "swarm_id": swarm_id,
        'data': json.dumps([]).encode('utf-8')})
    # Save swarmid
    execute(upload_file_action_id, swarm_id, 
        {'file_path': f"{swarm_id.instance_path}/swarm_id.json", "swarm_id": swarm_id,
        'data': json.dumps(swarm_id.model_dump_json()).encode('utf-8')})
