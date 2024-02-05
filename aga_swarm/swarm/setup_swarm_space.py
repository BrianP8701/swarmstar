'''

'''
from pydantic import validate_call
import json
from pathlib import Path
from typing import Any, Dict, Union

from aga_swarm.swarm.types import Swarm, SwarmState, SwarmHistory, Platform
from aga_swarm.swarm_utils.internal_package.get_swarm_defaults import get_default_action_space_metadata, get_default_memory_space_metadata
from aga_swarm.swarm_utils.swarm_space.file_operations.main import upload_swarm_space_file
from aga_swarm.swarm_utils.swarm_space.folder_operations.main import make_swarm_space_folder

def setup_swarm_space(openai_key: str, 
                        frontend_url: str, 
                        platform: str, 
                        swarm_space_root_path: str
                          ) -> Swarm:
    '''
        Configure the swarm to your enviroment!
        
        Any params you dont understand you can skip, you'll be 
        able to discuss them with a chatbot in the CLI.
        
        Args:
            openai_key (str)
            frontend_url (str)
            platform (str): Currently only support: ['mac', 'azure']
            swarm_space_root_path (str)
    '''
    platform = Platform(platform)
    
    required_keys_given_platform = {
        Platform.MAC: [],
        Platform.AZURE: ['azure_blob_storage_account_name', 
                         'azure_blob_storage_account_key', 
                         'azure_blob_storage_container_name', 
                         'azure_comsos_db_url', 
                         'azure_cosmos_db_key', 
                         'azure_cosmos_db_database_name']
    }
    
    swarm = Swarm(
        swarm_space_root_path=swarm_space_root_path,
        platform=platform,
        action_space_metadata_path="action_space_metadata_path",
        memory_space_metadata_path="memory_space_metadata_path",
        stage_path="stage_path",
        state_path="state_path",
        history_path="history_path",
        configs={
            'openai_key': openai_key,
            'frontend_url': frontend_url
        }
    )
    _setup_swarm(swarm, 
        json.dumps(get_default_action_space_metadata()).encode('utf-8'), 
        json.dumps(get_default_memory_space_metadata()).encode('utf-8'))
    
    return swarm



'''
    Private functions
'''    

def _setup_swarm(swarm: Swarm, action_space: bytes, memory_space: bytes) -> None:
    '''
        The "swarm space" is just the folder on your local machine 
        or blob storage used to your swarm blueprint and instances.
        
        All we are doing here is setting up the default swarm space
        in your chosen platform and folder.
    '''
    make_swarm_space_folder(swarm, f"{swarm.instance_path}/stage")
    swarm._upload_file(f"{swarm.instance_path}/action_space_metadata.json", action_space)
    swarm._upload_file(f"{swarm.instance_path}/memory_space_metadata.json", memory_space)
    swarm._upload_file(f"{swarm.instance_path}/state.json", SwarmState(nodes={}).model_dump_json().encode('utf-8'))
    swarm._upload_file(f"{swarm.instance_path}/history.json", SwarmHistory(frames=[]).model_dump_json().encode('utf-8'))
    swarm._upload_file(f"{swarm.instance_path}/swarm.json", swarm.model_dump_json().encode('utf-8'))
