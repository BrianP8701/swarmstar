"""
This is a common interface for file operations for the swarm space.

All file operations will happen within the swarm space root path.
"""
from __future__ import annotations

from importlib import import_module
from typing import TYPE_CHECKING

from swarmstar.utils.data.external_operations.imports import import_module_from_path

if TYPE_CHECKING:
    from swarmstar.swarm.types import SwarmConfig

platform_map = {
    "mac": "swarmstar.utils.data.file_operations.local_storage",
    "azure": "swarmstar.utils.data.file_operations.azure_blob_storage",
}

def get_file_operations_module(swarm: SwarmConfig):
    if swarm.file_operations_path:
        return import_module_from_path('file_operations_module', swarm.file_operations_path)
    else:
        platform = swarm.platform
        return import_module(platform_map[platform])

def delete_swarm_space_file(swarm: SwarmConfig, file_path: str) -> None:
    file_operations_module = get_file_operations_module(swarm)
    return file_operations_module.delete_file(swarm, file_path)


def move_swarm_space_file(
    swarm: SwarmConfig, file_path: str, new_file_path: str
) -> None:
    file_operations_module = get_file_operations_module(swarm)
    return file_operations_module.move_file(swarm, file_path, new_file_path)


def rename_swarm_space_file(
    swarm: SwarmConfig, file_path: str, new_file_name: str
) -> None:
    file_operations_module = get_file_operations_module(swarm)
    return file_operations_module.rename_file(swarm, file_path, new_file_name)


def upload_swarm_space_file(
    swarm: SwarmConfig, file_path: str, file_bytes: bytes
) -> None:
    file_operations_module = get_file_operations_module(swarm)
    return file_operations_module.upload_file(swarm, file_path, file_bytes)


def retrieve_swarm_space_file(swarm: SwarmConfig, file_path: str) -> bytes:
    file_operations_module = get_file_operations_module(swarm)
    return file_operations_module.retrieve_file(swarm, file_path)
