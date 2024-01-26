import os
from pydantic import validate_arguments

# Function to rename a file on a mac
@validate_arguments
def mac_rename_file(file_path: str, new_file_name: str) -> dict:
    try:
        # Extract directory path
        directory = os.path.dirname(file_path)
        # Create new file path
        new_file_path = os.path.join(directory, new_file_name)
        # Rename the file
        os.rename(file_path, new_file_path)
        return {'status_message': 'Success', 'error_message': ''}
    except Exception as e:
        return {'status_message': 'Failure', 'error_message': str(e)}

# Main section
@validate_arguments
def main(file_path: str, new_file_name: str) -> dict:
    return mac_rename_file(file_path, new_file_name)