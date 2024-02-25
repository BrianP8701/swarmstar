from __future__ import annotations

import os
import shutil
from typing import TYPE_CHECKING, List

if TYPE_CHECKING:
    from swarmstar.swarm.types import SwarmConfig


def delete_folder(swarm: SwarmConfig, folder_path: str) -> dict:
    try:
        shutil.rmtree(folder_path)
    except Exception as e:
        raise ValueError(f"Failed to delete folder: {str(e)}")


def list_folder(swarm: SwarmConfig, folder_path: str) -> List[str]:
    try:
        entries = os.listdir(folder_path)
        full_paths = [os.path.join(folder_path, entry) for entry in entries]
        return full_paths
    except Exception as e:
        raise ValueError(f"Failed to list folder: {str(e)}")


def make_folder(swarm: SwarmConfig, folder_path: str) -> dict:
    try:
        os.makedirs(folder_path, exist_ok=True)
    except Exception as e:
        raise ValueError(f"Failed to make folder: {str(e)}")


def move_folder(swarm: SwarmConfig, old_folder_path: str, new_folder_path: str) -> dict:
    try:
        shutil.move(old_folder_path, new_folder_path)
    except Exception as e:
        raise ValueError(f"Failed to move folder: {str(e)}")


def rename_folder(swarm: SwarmConfig, folder_path: str, new_folder_name: str) -> dict:
    try:
        os.rename(folder_path, new_folder_name)
    except Exception as e:
        raise ValueError(f"Failed to rename folder: {str(e)}")
