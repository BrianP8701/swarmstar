'''
The purpose of this module is to provide interoperable file operations for the swarm.

The swarm space can be located on different platforms, such as a local machine, a cloud server, or a remote machine.
This file provides a set of functions that can be used to perform file operations on the swarm space, regardless of the platform.
If on mac, linux or windows file operations will be performed locally according to the root path provided in the swarm config.
'''

import os
import shutil

from aga_swarm.swarm.types import SwarmConfig
from aga_swarm.swarm_utils.swarm_space_utils.paths import validate_and_adjust_swarm_space_path
    
def _local_delete_file(file_path: str) -> dict:
    try:
        os.remove(file_path)
        return {'success': True, 'error_message': ''}
    except Exception as e:
        return {'success': False, 'error_message': str(e)}

delete_file_map = {
    'local': _local_delete_file
}

def delete_swarm_space_file(swarm_config: SwarmConfig, file_path: str) -> dict:
    file_path = validate_and_adjust_swarm_space_path(file_path, swarm_config.swarm_space_root_path)
    platform = swarm_config.platform.value
    file_deletion_function = delete_file_map.get(platform, lambda _: {'success': False, 'error_message': 'Unsupported platform'})
    return file_deletion_function(file_path)




def _local_move_file(file_path: str, new_file_path: str) -> dict:
    try:
        shutil.move(file_path, new_file_path)
        return {'success': True, 'error_message': ''}
    except Exception as e:
        return {'success': False, 'error_message': str(e)}
    
move_file_map = {
    'local': _local_move_file
}

def move_swarm_space_file(swarm_config: SwarmConfig, file_path: str, new_file_path: str) -> dict:
    file_path = validate_and_adjust_swarm_space_path(file_path, swarm_config.swarm_space_root_path)
    platform = swarm_config.platform.value
    file_move_function = move_file_map.get(platform, lambda _, __: {'success': False, 'error_message': 'Unsupported platform'})
    return file_move_function(file_path, new_file_path)




def _local_rename_file(file_path: str, new_file_name: str) -> dict:
    try:
        # Extract directory path
        directory = os.path.dirname(file_path)
        # Create new file path
        new_file_path = os.path.join(directory, new_file_name)
        # Rename the file
        os.rename(file_path, new_file_path)
        return {'success': True, 'error_message': ''}
    except Exception as e:
        return {'success': False, 'error_message': str(e)}
    
rename_file_map = {
    'local': _local_rename_file
}

def rename_swarm_space_file(swarm_config: SwarmConfig, file_path: str, new_file_name: str) -> dict:
    file_path = validate_and_adjust_swarm_space_path(file_path, swarm_config.swarm_space_root_path)
    platform = swarm_config.platform.value
    file_rename_function = rename_file_map.get(platform, lambda _, __: {'success': False, 'error_message': 'Unsupported platform'})
    return file_rename_function(file_path, new_file_name)




def _local_upload_file(file_path: str, data: bytes) -> dict:
    try:
        # Ensure the directory exists
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        # Write the file
        with open(file_path, 'wb') as file:
            file.write(data)

        return {'success': True, 'error_message': ''}
    except Exception as e:
        return {'success': False, 'error_message': str(e)}
upload_file_map = {
    'local': _local_upload_file
}

def upload_swarm_space_file(swarm_config: SwarmConfig, file_path: str, data: bytes) -> dict:
    file_path = validate_and_adjust_swarm_space_path(file_path, swarm_config.swarm_space_root_path)
    platform = swarm_config.platform.value
    file_upload_function = upload_file_map.get(platform, lambda _, __: {'success': False, 'error_message': 'Unsupported platform'})
    return file_upload_function(file_path, data)



def _local_retrieve_file(file_path: str) -> dict:
    try:
        # Check if the file exists
        if not os.path.exists(file_path):
            return {
                'success': False,
                'error_message': 'File does not exist',
                'data': None
            }

        # Open the file in binary mode
        with open(file_path, 'rb') as file:
            file_data = file.read()

        # Return the file data
        return {
            'success': True,
            'error_message': '',
            'data': file_data
        }
    except Exception as e:
        # Handle any exception that occurs
        return {
            'success': False,
            'error_message': str(e),
            'data': None
        }

retrieve_file_map = {
    'local': _local_retrieve_file
}

def retrieve_swarm_space_file(swarm_config: SwarmConfig, file_path: str) -> dict:
    file_path = validate_and_adjust_swarm_space_path(file_path, swarm_config.swarm_space_root_path)
    platform = swarm_config.platform.value
    file_retrieval_function = retrieve_file_map.get(platform, lambda _: {'success': False, 'error_message': 'Unsupported platform'})
    return file_retrieval_function(file_path)