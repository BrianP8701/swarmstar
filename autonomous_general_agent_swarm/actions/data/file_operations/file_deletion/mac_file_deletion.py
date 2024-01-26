import os
import sys
import json

# Function to delete a file on a Mac
def mac_file_deletion(file_path):
    try:
        os.remove(file_path)
        return {'status_message': 'Success', 'error_message': ''}
    except Exception as e:
        return {'status_message': 'Failure', 'error_message': str(e)}

# Main section
if __name__ == '__main__':
    # Parse input
    input_args = json.loads(sys.argv[1])
    file_path = input_args.get('file_path', '')

    # Call the function and print the result
    result = mac_file_deletion(file_path)
    print(json.dumps(result))
