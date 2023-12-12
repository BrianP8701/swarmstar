from settings import Settings
import json
settings = Settings()

def save_python_code(code_type, python_code, name, description):
    if code_type == 0: # function
        save_path = settings.FUNCTIONS_PATH
    elif code_type == 1: # class
        save_path = settings.CLASSES_PATH
    elif code_type == 2: # script
        save_path = settings.SCRIPTS_PATH
    
    save_code_to_config(save_path, name, description, python_code)
    
        

def save_code_to_config(file_path, name, description, code):
    """
    Update a JSON file with a new key-value pair.

    :param file_path: Path to the JSON file.
    :param name: The key to add to the JSON dictionary.
    :param description: The description to add under the key.
    :param code: The code to add under the key.
    """
    try:
        # Load existing data from the JSON file
        with open(file_path, 'r') as file:
            data = json.load(file)

        # Check if data is a dictionary
        if not isinstance(data, dict):
            raise ValueError("JSON file does not contain a dictionary.")

        # Update the dictionary with the new key-value pair
        data[name] = {
            'description': description,
            'code': code
        }

        # Write the updated dictionary back to the JSON file
        with open(file_path, 'w') as file:
            json.dump(data, file, indent=4)

        print(f"File '{file_path}' updated successfully.")

    except FileNotFoundError:
        print(f"Error: The file '{file_path}' was not found.")
    except json.JSONDecodeError:
        print(f"Error: The file '{file_path}' does not contain valid JSON.")
    except ValueError as e:
        print(e)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")