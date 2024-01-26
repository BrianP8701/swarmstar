import os
import shutil
import sys
import json

# Function to delete a folder on a mac
def mac_delete_folder(folder_path):
    try:
        # Check if the folder exists
        if not os.path.exists(folder_path):
            return {'status_message': 'Failure', 'error_message': 'Folder does not exist'}
        
        # Check if the path is indeed a folder
        if not os.path.isdir(folder_path):
            return {'status_message': 'Failure', 'error_message': 'Path is not a folder'}
        
        # Remove the folder
        shutil.rmtree(folder_path)
        return {'status_message': 'Success', 'error_message': ''}
    except Exception as e:
        return {'status_message': 'Failure', 'error_message': str(e)}

# Main section
if __name__ == '__main__':
    # Parse input
    input_args = json.loads(sys.argv[1])
    folder_path = input_args['folder_path']
    
    # Call the function and print the result
    result = mac_delete_folder(folder_path)
    print(json.dumps(result))