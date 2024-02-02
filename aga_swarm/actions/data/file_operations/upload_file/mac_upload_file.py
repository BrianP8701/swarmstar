import os
from pydantic import validate_call, BaseModel

class Input(BaseModel):
    file_path: str
    data: bytes
    
class Output(BaseModel):
    success: bool
    error_message: str

# Function to upload a file to a Mac
def mac_file_upload(input: Input) -> Output:
    try:
        # Ensure the directory exists
        os.makedirs(os.path.dirname(input.file_path), exist_ok=True)

        # Write the file
        with open(input.file_path, 'wb') as file:
            file.write(input.data)

        return {'success': True, 'error_message': ''}
    except Exception as e:
        return {'success': False, 'error_message': str(e)}

# Main section
@validate_call
def main(input: Input) -> Output:
    return mac_file_upload(input)

