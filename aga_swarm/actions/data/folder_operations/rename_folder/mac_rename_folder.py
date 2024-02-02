import os
from pydantic import validate_call, BaseModel

class Input(BaseModel):
    folder_path: str
    new_folder_path: str
    
class Output(BaseModel):
    success: bool
    error_message: str

# Function to rename a folder on a Mac
def mac_rename_folder(input: Input) -> Output:
    try:
        os.rename(input.folder_path, input.new_folder_path)
        return {'success': True, 'error_message': ''}
    except Exception as e:
        return {'success': False, 'error_message': str(e)}

# Main section
@validate_call
def main(input: Input) -> Output:
    return mac_rename_folder(input)

