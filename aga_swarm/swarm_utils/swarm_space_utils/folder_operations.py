'''
The purpose of this module is to provide interoperable folder operations for the swarm.

The swarm space can be located on different platforms, such as a local machine, a cloud server, or a remote machine.
This file provides a set of functions that can be used to perform folder operations on the swarm space, regardless of the platform.
If on mac, linux or windows folder operations will be performed locally according to the root path provided in the swarm config.
'''

import os
import shutil

from aga_swarm.swarm.types import SwarmConfig
from aga_swarm.swarm_utils.swarm_space_utils.paths import validate_and_adjust_swarm_space_path




def _local_delete_folder(folder_path: str) -> dict:
    try:
        shutil.rmtree(folder_path)
        return {'success': True, 'error_message': ''}
    except Exception as e:
        return {'success': False, 'error_message': str(e)}

delete_folder_map = {
    'local': _local_delete_folder
}

def delete_swarm_space_folder(swarm_config: SwarmConfig, folder_path: str) -> dict:
    folder_path = validate_and_adjust_swarm_space_path(folder_path, swarm_config.swarm_space_root_path)
    platform = swarm_config.platform.value
    folder_deletion_function = delete_folder_map.get(platform, lambda _: {'success': False, 'error_message': 'Unsupported platform'})
    return folder_deletion_function(folder_path)




def _local_list_folder(folder_path: str) -> dict:
    try:
        files = os.listdir(folder_path)
        return {'success': True, 'error_message': '', 'data': files}
    except Exception as e:
        return {'success': False, 'error_message': str(e), 'data': None}

list_folder_map = {
    'local': _local_list_folder
}

def list_swarm_space_folder(swarm_config: SwarmConfig, folder_path: str) -> dict:
    folder_path = validate_and_adjust_swarm_space_path(folder_path, swarm_config.swarm_space_root_path)
    platform = swarm_config.platform.value
    folder_listing_function = list_folder_map.get(platform, lambda _: {'success': False, 'error_message': 'Unsupported platform', 'data': None})
    return folder_listing_function(folder_path)




def _local_make_folder(folder_path: str) -> dict:
    try:
        os.makedirs(folder_path, exist_ok=True)
        return {'success': True, 'error_message': ''}
    except Exception as e:
        return {'success': False, 'error_message': str(e)}

make_folder_map = {
    'local': _local_make_folder
}

def make_swarm_space_folder(swarm_config: SwarmConfig, folder_path: str) -> dict:
    folder_path = validate_and_adjust_swarm_space_path(folder_path, swarm_config.swarm_space_root_path)
    platform = swarm_config.platform.value
    folder_creation_function = make_folder_map.get(platform, lambda _: {'success': False, 'error_message': 'Unsupported platform'})
    return folder_creation_function(folder_path)




def _local_move_folder(folder_path: str, new_folder_path: str) -> dict:
    try:
        shutil.move(folder_path, new_folder_path)
        return {'success': True, 'error_message': ''}
    except Exception as e:
        return {'success': False, 'error_message': str(e)}

move_folder_map = {
    'local': _local_move_folder
}

def move_swarm_space_folder(swarm_config: SwarmConfig, folder_path: str, new_folder_path: str) -> dict:
    folder_path = validate_and_adjust_swarm_space_path(folder_path, swarm_config.swarm_space_root_path)
    platform = swarm_config.platform.value
    folder_move_function = move_folder_map.get(platform, lambda _, __: {'success': False, 'error_message': 'Unsupported platform'})
    return folder_move_function(folder_path, new_folder_path)




def _local_rename_folder(folder_path: str, new_folder_name: str) -> dict:
    try:
        # Extract directory path
        directory = os.path.dirname(folder_path)
        # Create new folder path
        new_folder_path = os.path.join(directory, new_folder_name)
        # Rename the folder
        os.rename(folder_path, new_folder_path)
        return {'success': True, 'error_message': ''}
    except Exception as e:
        return {'success': False, 'error_message': str(e)}

rename_folder_map = {
    'local': _local_rename_folder
}

def rename_swarm_space_folder(swarm_config: SwarmConfig, folder_path: str, new_folder_name: str) -> dict:
    folder_path = validate_and_adjust_swarm_space_path(folder_path, swarm_config.swarm_space_root_path)
    platform = swarm_config.platform.value
    folder_rename_function = rename_folder_map.get(platform, lambda _, __: {'success': False, 'error_message': 'Unsupported platform'})
    return folder_rename_function(folder_path, new_folder_name)
