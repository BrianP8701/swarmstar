import os
from pydantic import validate_call

# Function to delete a file on a Mac
def mac_file_deletion(file_path: str) -> dict:
    try:
        os.remove(file_path)
        return {'status_message': 'Success', 'error_message': ''}
    except Exception as e:
        return {'status_message': 'Failure', 'error_message': str(e)}

# Main section
@validate_call
def main(file_path: str) -> dict:
    return mac_file_deletion(file_path)
