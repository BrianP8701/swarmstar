import shutil
from pydantic import validate_call, BaseModel

class Input(BaseModel):
    folder_path: str
    new_folder_path: str
    
class Output(BaseModel):
    success: bool
    error_message: str

def mac_move_folder(input: Input) -> Output:
    try:
        # Move the folder to the new location
        shutil.move(input.folder_path, input.new_folder_path)
        return {'success': True, 'error_message': ''}
    except Exception as e:
        # Return failure message and the error
        return {'success': False, 'error_message': str(e)}

# Main section
@validate_call
def main(input: Input) -> Output:
    return mac_move_folder(input)
