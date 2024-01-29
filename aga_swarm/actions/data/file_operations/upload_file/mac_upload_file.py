import os
from pydantic import validate_call

# Function to upload a file to a Mac
def mac_file_upload(file_path: str, data: bytes) -> dict:
    try:
        # Ensure the directory exists
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        # Write the file
        with open(file_path, 'wb') as file:
            file.write(data)

        return {'status_message': 'Success', 'error_message': ''}
    except Exception as e:
        return {'status_message': 'Failure', 'error_message': str(e)}

# Main section
@validate_call
def main(file_path: str, data: bytes) -> dict:
    return mac_file_upload(file_path, data)