import os

# Function to list the contents of a folder on a mac
def mac_list_folder(folder_path):
    try:
        # List the contents of the folder
        contents = os.listdir(folder_path)
        return {'status_message': 'Success', 'error_message': '', 'contents': contents}
    except Exception as e:
        # Return error message if an exception occurs
        return {'status_message': 'Failure', 'error_message': str(e)}

# Main section
if __name__ == '__main__':
    # Example usage: Provide the folder path to list its contents
    folder_path = '/path/to/folder'
    result = mac_list_folder(folder_path)
    print(result)