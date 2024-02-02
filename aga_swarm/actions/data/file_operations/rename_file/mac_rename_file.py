import os
from pydantic import validate_call, BaseModel

class Input(BaseModel):
    file_path: str
    new_file_name: str

class Output(BaseModel):
    success: bool
    error_message: str

# Function to rename a file on a mac
def mac_rename_file(input: Input) -> Output:
    try:
        # Extract directory path
        directory = os.path.dirname(input.file_path)
        # Create new file path
        new_file_path = os.path.join(directory, input.new_file_name)
        # Rename the file
        os.rename(input.file_path, new_file_path)
        return {'success': True, 'error_message': ''}
    except Exception as e:
        return {'success': False, 'error_message': str(e)}

# Main section
@validate_call
def main(input: Input) -> Output:
    return mac_rename_file(input)
