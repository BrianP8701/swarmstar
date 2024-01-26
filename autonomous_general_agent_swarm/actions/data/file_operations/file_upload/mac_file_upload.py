import os

# Function to upload a file to a Mac
def mac_file_upload(file_path, data):
    try:
        # Ensure the directory exists
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        # Write the file
        with open(file_path, 'wb') as file:
            file.write(data.read())

        return {'status_message': 'Success'}
    except Exception as e:
        return {'status_message': 'Failure', 'error_message': str(e)}

# Main section
if __name__ == '__main__':
    # Example usage
    file_path = '/path/to/your/file.txt'  # Replace with your file path
    data = open(file_path, 'rb')  # Replace with your file data
    result = mac_file_upload(file_path, data)
    print(result)
    data.close()