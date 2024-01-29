import shutil
from pydantic import validate_call

# Function to move a folder on a mac
def mac_move_folder(folder_path: str, new_folder_path: str) -> dict:
    try:
        # Move the folder to the new location
        shutil.move(folder_path, new_folder_path)
        return {'status_message': 'Success', 'error_message': ''}
    except Exception as e:
        # Return failure message and the error
        return {'status_message': 'Failure', 'error_message': str(e)}

# Main section
@validate_call
def main(folder_path: str, new_folder_path: str) -> dict:
    return mac_move_folder(folder_path, new_folder_path)
