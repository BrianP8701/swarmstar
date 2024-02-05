import os
import shutil

from aga_swarm.swarm.types import Swarm

def delete_file(swarm: Swarm, file_path: str) -> dict:
    try:
        os.remove(file_path)
        return {'success': True, 'error_message': ''}
    except Exception as e:
        return {'success': False, 'error_message': str(e)}
    
def move_file(swarm: Swarm, file_path: str, new_file_path: str) -> dict:
    try:
        shutil.move(file_path, new_file_path)
        return {'success': True, 'error_message': ''}
    except Exception as e:
        return {'success': False, 'error_message': str(e)}
    
def rename_file(swarm: Swarm, file_path: str, new_file_name: str) -> dict:
    try:
        directory = os.path.dirname(file_path)
        new_file_path = os.path.join(directory, new_file_name)
        os.rename(file_path, new_file_path)
        return {'success': True, 'error_message': ''}
    except Exception as e:
        return {'success': False, 'error_message': str(e)}
    
def upload_file(swarm: Swarm, file_path: str, file_bytes: bytes) -> dict:
    try:
        with open(file_path, 'wb') as file:
            file.write(file_bytes)
        return {'success': True, 'error_message': ''}
    except Exception as e:
        return {'success': False, 'error_message': str(e)}
    
def retrieve_file(swarm: Swarm, file_path: str) -> dict:
    try:
        with open(file_path, 'rb') as file:
            file_bytes = file.read()
        return {'success': True, 'error_message': '', 'data': file_bytes}
    except Exception as e:
        return {'success': False, 'error_message': str(e), 'data': None}