import os
import shutil

# Function to move a folder on a mac
def mac_move_folder(folder_path, new_folder_path):
    try:
        # Move the folder to the new location
        shutil.move(folder_path, new_folder_path)
        return {'status_message': 'Success'}
    except Exception as e:
        # Return failure message and the error
        return {'status_message': 'Failure', 'error_message': str(e)}

# Main section
if __name__ == '__main__':
    # Example usage:
    # folder_path = '/path/to/current/folder'
    # new_folder_path = '/path/to/new/folder'
    # result = mac_move_folder(folder_path, new_folder_path)
    # print(result)
    pass
