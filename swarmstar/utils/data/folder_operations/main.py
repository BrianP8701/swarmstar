"""
This is a common interface for folder operations for the swarm space.

All folder operations will happen within the swarm space root path.
"""
from __future__ import annotations

from importlib import import_module
from typing import TYPE_CHECKING, List

from swarmstar.utils.data.external_operations.imports import import_module_from_path

if TYPE_CHECKING:
    from swarmstar.types import SwarmConfig

platform_map = {
    "mac": "swarmstar.utils.data.folder_operations.local_storage",
    "azure": "swarmstar.utils.data.folder_operations.azure_blob_storage",
}

def get_folder_operations_module(swarm: SwarmConfig):
    if swarm.folder_operations_path:
        return import_module_from_path('folder_operations_module', swarm.folder_operations_path)
    else:
        platform = swarm.platform
        return import_module(platform_map[platform])


def delete_swarm_space_folder(swarm: SwarmConfig, folder_path: str) -> None:
    folder_operations_module = get_folder_operations_module(swarm)
    return folder_operations_module.delete_folder(swarm, folder_path)

def list_swarm_space_folder(swarm: SwarmConfig, folder_path: str) -> List[str]:
    folder_operations_module = get_folder_operations_module(swarm)
    return folder_operations_module.list_folder(swarm, folder_path)

def make_swarm_space_folder(swarm: SwarmConfig, folder_path: str) -> None:
    folder_operations_module = get_folder_operations_module(swarm)
    return folder_operations_module.make_folder(swarm, folder_path)

def move_swarm_space_folder(
    swarm: SwarmConfig, folder_path: str, new_folder_path: str
) -> None:
    folder_operations_module = get_folder_operations_module(swarm)
    return folder_operations_module.move_folder(swarm, folder_path, new_folder_path)

def rename_swarm_space_folder(
    swarm: SwarmConfig, folder_path: str, new_folder_name: str
) -> None:
    folder_operations_module = get_folder_operations_module(swarm)
    return folder_operations_module.rename_folder(swarm, folder_path, new_folder_name)
