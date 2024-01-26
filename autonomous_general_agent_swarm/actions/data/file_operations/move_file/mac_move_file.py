import os
import shutil

# Function to move a file on a mac
def mac_move_file(file_path, new_file_path):
    try:
        # Move the file
        shutil.move(file_path, new_file_path)
        return {'status_message': 'Success', 'error_message': ''}
    except Exception as e:
        # Return the error message if an exception occurs
        return {'status_message': 'Failure', 'error_message': str(e)}

# Main section
if __name__ == '__main__':
    # Example usage
    input_params = {
        'file_path': '/path/to/old/location/file.txt',
        'new_file_path': '/path/to/new/location/file.txt'
    }
    result = mac_move_file(**input_params)
    print(result)