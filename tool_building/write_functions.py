'''
Temporary file to write and add functions to the functions.json file manually. Write your function starting from line 40
'''

import json
from settings import Settings

settings = Settings()

def save_python_file_to_json(file_path, json_path, name, description, start_line):
    """
    Save a Python file to a JSON file with an additional description.

    :param file_path: Path to the Python file.
    :param json_path: Path to the JSON file.
    :param name: The key to add to the JSON dictionary.
    :param description: The description to add under the key.
    :param start_line: The line number from which to start reading the Python file.
    """
    # Read the Python file from a specific line number to the end
    try:
        with open(file_path, 'r') as file:
            # Skip lines until the start_line
            for _ in range(start_line - 1):
                next(file)
            file_content = file.read()
    except IOError as e:
        print(f"Error reading file {file_path}: {e}")
        return

    # Load the existing JSON file into a dictionary
    try:
        with open(json_path, 'r') as json_file:
            data = json.load(json_file)
    except IOError:
        print(f"Error reading JSON file {json_path}. A new file will be created.")
        data = {}

    # Update the dictionary with the new key-value pair
    data[name] = {
        'code': file_content,
        'description': description
    }

    # Write the updated dictionary back to the JSON file
    try:
        with open(json_path, 'w') as json_file:
            json.dump(data, json_file, indent=4)
    except IOError as e:
        print(f"Error writing to JSON file {json_path}: {e}")

description = ''
save_python_file_to_json('tool_building/write_functions.py', settings.FUNCTIONS_PATH, 'save_python_code', description, 56)

# Write function below: 
from swarm.memory.save_code import save_python_code 
async def save_python_code(code_type, python_code, name, description):
    save_python_code(code_type, python_code, name, description)