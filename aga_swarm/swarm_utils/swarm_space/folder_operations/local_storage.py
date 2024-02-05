import os
import shutil

from aga_swarm.swarm.types import Swarm

def delete_folder(folder_path: str) -> dict:
    try:
        shutil.rmtree(folder_path)
        return {'success': True, 'error_message': ''}
    except Exception as e:
        return {'success': False, 'error_message': str(e)}
    
def list_folder(folder_path: str) -> dict:
    try:
        entries = os.listdir(folder_path)
        full_paths = [os.path.join(folder_path, entry) for entry in entries]
        return {'success': True, 'error_message': '', 'paths': full_paths}
    except Exception as e:
        return {'success': False, 'error_message': str(e), 'paths': None}
    
def make_folder(folder_path: str) -> dict:
    try:
        os.makedirs(folder_path, exist_ok=True)
        return {'success': True, 'error_message': ''}
    except Exception as e:
        return {'success': False, 'error_message': str(e)}
    
def move_folder(old_folder_path: str, new_folder_path: str) -> dict:
    try:
        shutil.move(old_folder_path, new_folder_path)
        return {'success': True, 'error_message': ''}
    except Exception as e:
        return {'success': False, 'error_message': str(e)}
    
def rename_folder(folder_path: str, new_folder_name: str) -> dict:
    try:
        os.rename(folder_path, new_folder_name)
        return {'success': True, 'error_message': ''}
    except Exception as e:
        return {'success': False, 'error_message': str(e)}
    