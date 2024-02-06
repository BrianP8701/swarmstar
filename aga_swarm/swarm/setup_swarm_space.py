'''
Swarm setup includes:
    1. Setting up storage for the swarm space on your chosen platform
    2. Creating a swarm object
    
The swarm space contains all the metadata for the swarm spaces, a stage
for generated content, a place to store the state of the swarm, and more.
    
The swarm object contains keys and configs for your personal swarm space. It's
passed around between every node and action. Keep it safe and private!
'''

import os

from aga_swarm.swarm.types import Swarm, Platform
from aga_swarm.utils.data.kv_operations.sqlite3 import create_or_open_kv_db
from aga_swarm.utils.data.file_operations.local_storage import upload_file
from aga_swarm.utils.data.file_operations.azure_blob_storage import upload_file

def setup_swarm_space(openai_key: str, 
                        frontend_url: str, 
                        platform: str, 
                        swarm_space_root_path: str
                          ) -> Swarm:
    try:
        platform = Platform(platform)
    except ValueError:
        raise ValueError(f'Invalid platform: {platform}')
    
    platform_map = {
        'mac': setup_mac_swarm_space,
        'azure': setup_azure_swarm_space,
    }
    
    swarm = platform_map[platform](openai_key, frontend_url, swarm_space_root_path)
    
def setup_mac_swarm_space(openai_key: str, 
                        frontend_url: str, 
                        swarm_space_root_path: str
                          ) -> Swarm:
    print('Setting up swarm space for mac')
    
    '''
    things we need for mac: root path, 
    '''
    
    def is_valid_empty_folder(path: str) -> bool:
        if not os.path.exists(path):
            os.makedirs(path)
            return True
        else:
            if not os.path.isdir(path):
                raise ValueError(f'Invalid path: {path}')
            if os.listdir(path):
                raise ValueError(f'Folder is not empty: {path}')
            return True

    root_path = get_user_input_with_validation(
        primary_message='''The swarm space root path is where all data and 
        interactions of this swarm instance will be stored. All swarm actions will 
        be confined to this space. Enter the swarm space root path: ''',
        retry_message='Invalid path. Please enter a valid path. The folder should be empty.',
        validation_function=is_valid_empty_folder
    )
    
    sqlite3_db_path = f'{root_path}/swarm_default_kv_store.db'
    create_or_open_kv_db(sqlite3_db_path)
    
    return Swarm(
        swarm_space_root_path=root_path,
        platform=Platform.MAC,
        
    )
    

def setup_azure_swarm_space(openai_key: str,
                            frontend_url: str,
                            swarm_space_root_path: str
                            ) -> Swarm:
    pass
    
def get_user_input_with_validation(primary_message: str, retry_message: str, validation_function):
    while True:
        print(primary_message)
        user_input = input()
        try:
            validation_function(user_input)
            return user_input
        except ValueError:
            print(retry_message)

    
setup_swarm_space(openai_key='openai_key', frontend_url='frontend_url', platform='mac', swarm_space_root_path='swarm_space_root_path') == None