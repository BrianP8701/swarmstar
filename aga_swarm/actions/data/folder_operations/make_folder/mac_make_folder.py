import os
from pydantic import validate_call

# Function to create a folder on a mac
def mac_make_folder(folder_path: str) -> dict:
    try:
        # Create the directory if it does not exist
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
            return {'status_message': 'Success', 'error_message': ''}
        else:
            return {'status_message': 'Failure', 'error_message': 'Folder already exists.'}
    except Exception as e:
        # Return failure with an error message
        return {'status_message': 'Failure', 'error_message': str(e)}

# Main section
@validate_call
def main(folder_path: str) -> dict:
    return mac_make_folder(folder_path)
