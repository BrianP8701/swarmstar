import os
from pydantic import validate_call

# Function to retrieve a file from a Mac
def mac_file_retrieval(file_path: str) -> dict:
    try:
        # Check if the file exists
        if not os.path.exists(file_path):
            return {
                'status_message': 'Failure',
                'error_message': 'File does not exist',
                'data': None
            }

        # Open the file in binary mode
        with open(file_path, 'rb') as file:
            file_data = file.read()

        # Return the file data
        return {
            'status_message': 'Success',
            'error_message': '',
            'data': file_data
        }
    except Exception as e:
        # Handle any exception that occurs
        return {
            'status_message': 'Failure',
            'error_message': str(e),
            'data': None
        }

# Main section
@validate_call
def main(file_path: str) -> dict:
    return mac_file_retrieval(file_path)