'''
This is a common interface for folder operations for the swarm space.

All folder operations will happen within the swarm space root path.
'''

from importlib import import_module
from typing import List

from aga_swarm.swarm.types.swarm import Swarm
from aga_swarm.utils.data.paths import validate_and_adjust_swarm_space_path


platform_map = {
    'local': 'aga_swarm.swarm_utils.swarm_space_utils.folder_operations.local_storage',
    'azure': 'aga_swarm.swarm_utils.swarm_space_utils.folder_operations.azure_blob_storage',
}

def delete_swarm_space_folder(swarm: Swarm, folder_path: str) -> None:
    platform = swarm.platform.value
    folder_path = validate_and_adjust_swarm_space_path(folder_path, swarm.swarm_space_root_path)
    folder_operations_module = import_module(platform_map[platform])
    return folder_operations_module.delete_folder(swarm, folder_path)

def list_swarm_space_folder(swarm: Swarm, folder_path: str) -> List[str]:
    platform = swarm.platform.value
    folder_path = validate_and_adjust_swarm_space_path(folder_path, swarm.swarm_space_root_path)
    folder_operations_module = import_module(platform_map[platform])
    return folder_operations_module.list_folder(swarm, folder_path)

def make_swarm_space_folder(swarm: Swarm, folder_path: str) -> None:
    platform = swarm.platform.value
    folder_path = validate_and_adjust_swarm_space_path(folder_path, swarm.swarm_space_root_path)
    folder_operations_module = import_module(platform_map[platform])
    return folder_operations_module.make_folder(swarm, folder_path)

def move_swarm_space_folder(swarm: Swarm, folder_path: str, new_folder_path: str) -> None:
    platform = swarm.platform.value
    folder_path = validate_and_adjust_swarm_space_path(folder_path, swarm.swarm_space_root_path)
    new_folder_path = validate_and_adjust_swarm_space_path(new_folder_path, swarm.swarm_space_root_path)
    folder_operations_module = import_module(platform_map[platform])
    return folder_operations_module.move_folder(swarm, folder_path, new_folder_path)

def rename_swarm_space_folder(swarm: Swarm, folder_path: str, new_folder_name: str) -> None:
    platform = swarm.platform.value
    folder_path = validate_and_adjust_swarm_space_path(folder_path, swarm.swarm_space_root_path)
    new_folder_name = validate_and_adjust_swarm_space_path(new_folder_name, swarm.swarm_space_root_path)
    folder_operations_module = import_module(platform_map[platform])
    return folder_operations_module.rename_folder(swarm, folder_path, new_folder_name)