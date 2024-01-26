import os

# Function to rename a file on a mac
def mac_rename_file(file_path, new_file_name):
    try:
        # Extract directory path
        directory = os.path.dirname(file_path)
        # Create new file path
        new_file_path = os.path.join(directory, new_file_name)
        # Rename the file
        os.rename(file_path, new_file_path)
        return {'status_message': 'Success'}
    except Exception as e:
        return {'status_message': 'Failure', 'error_message': str(e)}

# Main section
if __name__ == '__main__':
    # Example usage
    input_data = {'file_path': '/path/to/oldfile.txt', 'new_file_name': 'newfile.txt'}
    result = mac_rename_file(**input_data)
    print(result)