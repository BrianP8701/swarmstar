from pydantic import validate_arguments
import json
import os

from aga_swarm.core.swarm.types import SwarmBlueprint, SwarmInstance, SwarmID
from aga_swarm.core.swarm.swarm_utils import get_default_action_space_metadata, get_default_memory_space_metadata
from aga_swarm.actions.swarm.action_types.internal_swarm_default_action import internal_swarm_default_action as execute

@validate_arguments
def build_swarm_blueprint(blueprint_name: str, openai_key: str, frontend_url: str, platform: str, root_path: str) -> SwarmBlueprint:
    '''
    Create and configure your swarm with your environment and data. 
    
    Parameters:
        - blueprint_name (str)
        - openai_key (str)
        - frontend_url (str): The URL for the frontend interface of the swarm.
        - platform (str): Choose between: ['mac', 'windows', 'linux', 'azure', 'gcp', 'aws']
        - root_path (str): The root path for this swarm blueprint and it's instances to be stored.
        
    This will create the root path if it does not exist. This folder should be empty before creating a swarm blueprint.
    This folder will be used to store all swarm instances.
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
    _setup_swarm_space(swarm_id)
    return swarm_id

@validate_arguments
def create_swarm_instance(swarm_blueprint: SwarmBlueprint, instance_name: str) -> dict:
    '''
    Create a new instance of a swarm blueprint.
    '''
    _setup_swarm_instance_space(swarm_blueprint.model_dump(), instance_name)
    
    
    
'''
    Private functions
'''    

@validate_arguments
def _setup_swarm_space(swarm_id: SwarmID) -> dict:
    # Create swarm instance folder
    execute(f'aga_swarm/actions/data/folder_operations/make_folder/make_folder.py', 
            swarm_id, 
            {'folder_path': swarm_id.instance_path, "swarm_id": swarm_id})
    # Create stage
    execute(f'aga_swarm/actions/data/folder_operations/make_folder/make_folder.py', 
            swarm_id, 
            {'folder_path': f"{swarm_id.instance_path}/stage", "swarm_id": swarm_id})
    # Create action space metadata
    execute(f'aga_swarm/actions/data/file_operations/upload_file/upload_file.py', 
            swarm_id, 
            {'file_path': f"{swarm_id.instance_path}/action_space_metadata.json", "swarm_id": swarm_id,
            'data': json.dumps(get_default_action_space_metadata()).encode('utf-8')})
    # Create memory space metadata
    execute(f'aga_swarm/actions/data/file_operations/upload_file/upload_file.py', 
            swarm_id, 
            {'file_path': f"{swarm_id.instance_path}/memory_space_metadata.json", "swarm_id": swarm_id,
            'data': json.dumps(get_default_memory_space_metadata()).encode('utf-8')})
    # Create state
    execute(f'aga_swarm/actions/data/file_operations/upload_file/upload_file.py', 
        swarm_id, 
        {'file_path': f"{swarm_id.instance_path}/state.json", "swarm_id": swarm_id,
        'data': json.dumps({}).encode('utf-8')})
    # Create history
    execute(f'aga_swarm/actions/data/file_operations/upload_file/upload_file.py', 
        swarm_id, 
        {'file_path': f"{swarm_id.instance_path}/history.json", "swarm_id": swarm_id,
        'data': json.dumps([]).encode('utf-8')})

@validate_arguments
def _setup_swarm_instance_space(swarm_instance: SwarmInstance, instance_name: str) -> dict:
    # Create swarm instance folder. This is the swarm instance's root path.
    execute(f'aga_swarm/actions/data/folder_operations/make_folder/make_folder.py', 
            swarm_instance, 
            {'folder_path': f"{swarm_instance['configs']['root_path']}/{instance_name}", "swarm": swarm_instance})
    swarm_instance['configs']['root_path'] = f"{swarm_instance['configs']['root_path']}/{swarm_instance['swarm_instance']}"
    # Create stage
    execute(f'aga_swarm/actions/data/folder_operations/make_folder/make_folder.py', 
            swarm_instance, 
            {'folder_path': f"{swarm_instance['configs']['root_path']}/{instance_name}/stage", "swarm": swarm_instance})
    swarm_instance['configs']['stage_path'] = f"{swarm_instance['configs']['root_path']}/{swarm_instance['swarm_instance']}/stage"
    # Create action space
    execute(f'aga_swarm/actions/data/file_operations/upload_file/upload_file.py', 
            swarm_instance, 
            {'file_path': f"{swarm_instance['configs']['root_path']}/{instance_name}/action_space/action_space.json", "swarm": swarm_instance},
            {'data': json.dumps(swarm_instance['action_space']).encode('utf-8')})
    
    # Upload swarm instance as json file
    swarm_blueprint_str = json.dumps(swarm_instance)
    swarm_blueprint_bytes = swarm_blueprint_str.encode('utf-8')
    execute(f'aga_swarm/actions/data/file_operations/upload_file/upload_file.py',
            swarm_instance,
            {'file_path': f"{swarm_instance['configs']['root_path']}/{instance_name}/swarm_blueprint.json",
            'data': swarm_blueprint_bytes, "swarm": swarm_instance})