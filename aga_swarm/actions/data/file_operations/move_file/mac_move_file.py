import shutil
from pydantic import validate_call

# Function to move a file on a mac
def mac_move_file(file_path: str, new_file_path: str) -> dict:
    try:
        # Move the file
        shutil.move(file_path, new_file_path)
        return {'status_message': 'Success', 'error_message': ''}
    except Exception as e:
        # Return the error message if an exception occurs
        return {'status_message': 'Failure', 'error_message': str(e)}

# Main section
@validate_call
def main(file_path: str, new_file_path: str) -> dict:
    return mac_move_file(file_path, new_file_path)