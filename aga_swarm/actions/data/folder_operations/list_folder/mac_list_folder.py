import os
from pydantic import validate_call, BaseModel
from typing import List

class Input(BaseModel):
    folder_path: str

class Output(BaseModel):
    success: bool
    error_message: str
    files: List[str]

# Function to list the contents of a folder on a mac
def mac_list_folder(input: Input) -> Output:
    try:
        # List the contents of the folder
        contents = os.listdir(input.folder_path)
        return {'success': True, 'error_message': '', 'contents': contents}
    except Exception as e:
        # Return error message if an exception occurs
        return {'success': False, 'error_message': str(e), 'contents': []}

# Main section
@validate_call
def main(input: Input) -> Output:
    return mac_list_folder(input)
