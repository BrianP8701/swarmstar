"""
This is a common interface for folder operations for the swarm space.

All folder operations will happen within the swarm space root path.
"""
from __future__ import annotations

from importlib import import_module
from typing import TYPE_CHECKING, List

from swarmstar.utils.data.paths import validate_and_adjust_swarm_space_path

if TYPE_CHECKING:
    from swarmstar.swarm.types import SwarmConfig

platform_map = {
    "mac": "swarmstar.utils.data.folder_operations.local_storage",
    "azure": "swarmstar.utils.data.folder_operations.azure_blob_storage",
}


def delete_swarm_space_folder(swarm: SwarmConfig, folder_path: str) -> None:
    platform = swarm.platform
    folder_path = validate_and_adjust_swarm_space_path(
        folder_path, swarm.swarm_space_root_path
    )
    folder_operations_module = import_module(platform_map[platform])
    return folder_operations_module.delete_folder(swarm, folder_path)


def list_swarm_space_folder(swarm: SwarmConfig, folder_path: str) -> List[str]:
    platform = swarm.platform
    folder_path = validate_and_adjust_swarm_space_path(
        folder_path, swarm.swarm_space_root_path
    )
    folder_operations_module = import_module(platform_map[platform])
    return folder_operations_module.list_folder(swarm, folder_path)


def make_swarm_space_folder(swarm: SwarmConfig, folder_path: str) -> None:
    platform = swarm.platform
    folder_path = validate_and_adjust_swarm_space_path(
        folder_path, swarm.swarm_space_root_path
    )
    folder_operations_module = import_module(platform_map[platform])
    return folder_operations_module.make_folder(swarm, folder_path)


def move_swarm_space_folder(
    swarm: SwarmConfig, folder_path: str, new_folder_path: str
) -> None:
    platform = swarm.platform
    folder_path = validate_and_adjust_swarm_space_path(
        folder_path, swarm.swarm_space_root_path
    )
    new_folder_path = validate_and_adjust_swarm_space_path(
        new_folder_path, swarm.swarm_space_root_path
    )
    folder_operations_module = import_module(platform_map[platform])
    return folder_operations_module.move_folder(swarm, folder_path, new_folder_path)


def rename_swarm_space_folder(
    swarm: SwarmConfig, folder_path: str, new_folder_name: str
) -> None:
    platform = swarm.platform
    folder_path = validate_and_adjust_swarm_space_path(
        folder_path, swarm.swarm_space_root_path
    )
    new_folder_name = validate_and_adjust_swarm_space_path(
        new_folder_name, swarm.swarm_space_root_path
    )
    folder_operations_module = import_module(platform_map[platform])
    return folder_operations_module.rename_folder(swarm, folder_path, new_folder_name)
