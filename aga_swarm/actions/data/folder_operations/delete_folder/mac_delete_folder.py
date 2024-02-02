import os
import shutil
from pydantic import validate_call, BaseModel

class Input(BaseModel):
    folder_path: str
    
class Output(BaseModel):
    success: bool
    error_message: str

def mac_delete_folder(input: Input) -> Output:
    try:
        # Check if the folder exists
        if not os.path.exists(input.folder_path):
            return {'success': False, 'error_message': 'Folder does not exist'}
        
        # Check if the path is indeed a folder
        if not os.path.isdir(input.folder_path):
            return {'success': False, 'error_message': 'Path is not a folder'}
        
        # Remove the folder
        shutil.rmtree(input.folder_path)
        return {'success': True, 'error_message': ''}
    except Exception as e:
        return {'success': False, 'error_message': str(e)}

@validate_call
def main(input: Input) -> Output:
    return mac_delete_folder(input)

