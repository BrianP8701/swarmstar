import os
import shutil
from pydantic import validate_call

# Function to delete a folder on a mac
def mac_delete_folder(folder_path: str) -> dict:
    try:
        # Check if the folder exists
        if not os.path.exists(folder_path):
            return {'status_message': 'Failure', 'error_message': 'Folder does not exist'}
        
        # Check if the path is indeed a folder
        if not os.path.isdir(folder_path):
            return {'status_message': 'Failure', 'error_message': 'Path is not a folder'}
        
        # Remove the folder
        shutil.rmtree(folder_path)
        return {'status_message': 'Success', 'error_message': ''}
    except Exception as e:
        return {'status_message': 'Failure', 'error_message': str(e)}

# Main section
@validate_call
def main(folder_path: str) -> dict:
    return mac_delete_folder(folder_path)