import os
from pydantic import validate_call, BaseModel

class Input(BaseModel):
    file_path: str
    
class Output(BaseModel):
    success: bool
    error_message: str

# Function to delete a file on a Mac
def mac_file_deletion(input: Input) -> Output:
    try:
        os.remove(input.file_path)
        return {'success': True, 'error_message': ''}
    except Exception as e:
        return {'success': False, 'error_message': str(e)}

# Main section
@validate_call
def main(input: Input) -> Output:
    return mac_file_deletion(input)
