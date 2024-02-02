import os
from pydantic import validate_call, BaseModel

class Input(BaseModel):
    folder_path: str
    
class Output(BaseModel):
    success: bool
    error_message: str

# Function to create a folder on a mac
def mac_make_folder(input: Input) -> Output:
    try:
        # Create the directory if it does not exist
        if not os.path.exists(input.folder_path):
            os.makedirs(input.folder_path)
            return {'success': True, 'error_message': ''}
        else:
            return {'success': False, 'error_message': 'Folder already exists.'}
    except Exception as e:
        # Return failure with an error message
        return {'success': False, 'error_message': str(e)}

# Main section
@validate_call
def main(input: Input) -> Output:
    return mac_make_folder(input)
