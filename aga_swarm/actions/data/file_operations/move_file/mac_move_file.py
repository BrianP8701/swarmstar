import shutil
from pydantic import validate_call, BaseModel

class Input(BaseModel):
    file_path: str
    new_file_path: str
    
class Output(BaseModel):
    success: bool
    error_message: str

# Function to move a file on a mac
def mac_move_file(input: Input) -> Output:
    try:
        # Move the file
        shutil.move(input.file_path, input.new_file_path)
        return {'success': True, 'error_message': ''}
    except Exception as e:
        # Return the error message if an exception occurs
        return {'success': False, 'error_message': str(e)}

# Main section
@validate_call
def main(input: Input) -> Output:
    return mac_move_file(input)

