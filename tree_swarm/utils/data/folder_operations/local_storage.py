from __future__ import annotations
from typing import TYPE_CHECKING, List
import os
import shutil

if TYPE_CHECKING:
    from tree_swarm.swarm.types import Swarm

def delete_folder(folder_path: str) -> dict:
    try:
        shutil.rmtree(folder_path)
    except Exception as e:
        raise ValueError(f'Failed to delete folder: {str(e)}')
    
def list_folder(folder_path: str) -> List[str]:
    try:
        entries = os.listdir(folder_path)
        full_paths = [os.path.join(folder_path, entry) for entry in entries]
        return full_paths
    except Exception as e:
        raise ValueError(f'Failed to list folder: {str(e)}')
    
def make_folder(folder_path: str) -> dict:
    try:
        os.makedirs(folder_path, exist_ok=True)
    except Exception as e:
        raise ValueError(f'Failed to make folder: {str(e)}')
    
def move_folder(old_folder_path: str, new_folder_path: str) -> dict:
    try:
        shutil.move(old_folder_path, new_folder_path)
    except Exception as e:
        raise ValueError(f'Failed to move folder: {str(e)}')
    
def rename_folder(folder_path: str, new_folder_name: str) -> dict:
    try:
        os.rename(folder_path, new_folder_name)
    except Exception as e:
        raise ValueError(f'Failed to rename folder: {str(e)}')
