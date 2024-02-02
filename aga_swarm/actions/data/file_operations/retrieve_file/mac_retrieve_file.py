import os
from pydantic import validate_call, BaseModel

class Input(BaseModel):
    file_path: str
    
class Output(BaseModel):
    success: bool
    error_message: str
    data: bytes

# Function to retrieve a file from a Mac
def mac_file_retrieval(input: Input) -> Output:
    try:
        # Check if the file exists
        if not os.path.exists(input.file_path):
            return {
                'success': False,
                'error_message': 'File does not exist',
                'data': None
            }

        # Open the file in binary mode
        with open(input.file_path, 'rb') as file:
            file_data = file.read()

        # Return the file data
        return {
            'success': True,
            'error_message': '',
            'data': file_data
        }
    except Exception as e:
        # Handle any exception that occurs
        return {
            'success': False,
            'error_message': str(e),
            'data': None
        }

# Main section
@validate_call
def main(input: Input) -> Output:
    return mac_file_retrieval(input)

