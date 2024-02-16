from __future__ import annotations
from typing import TYPE_CHECKING
import os
import shutil

if TYPE_CHECKING:
    from tree_swarm.swarm.types import Swarm

def delete_file(swarm: Swarm, file_path: str) -> None:
    try:
        os.remove(file_path)
    except Exception as e:
        raise ValueError(f'Failed to delete file: {str(e)}')
    
def move_file(swarm: Swarm, file_path: str, new_file_path: str) -> None:
    try:
        shutil.move(file_path, new_file_path)
    except Exception as e:
        raise ValueError(f'Failed to move file: {str(e)}')
    
def rename_file(swarm: Swarm, file_path: str, new_file_name: str) -> None:
    try:
        directory = os.path.dirname(file_path)
        new_file_path = os.path.join(directory, new_file_name)
        os.rename(file_path, new_file_path)
    except Exception as e:
        raise ValueError(f'Failed to rename file: {str(e)}')
    
def upload_file(swarm: Swarm, file_path: str, file_bytes: bytes) -> None:
    try:
        with open(file_path, 'wb') as file:
            file.write(file_bytes)
    except Exception as e:
        raise ValueError(f'Failed to upload file: {str(e)}')
    
def retrieve_file(swarm: Swarm, file_path: str) -> bytes:
    try:
        with open(file_path, 'rb') as file:
            file_bytes = file.read()
        return file_bytes
    except Exception as e:
        raise ValueError(f'Failed to retrieve file: {str(e)}')

