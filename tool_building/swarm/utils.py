import json
from settings import Settings

settings = Settings()

def update_python_script_test_success(code_key, autonomous_on, success_data):
    # Load the existing JSON data
    try:
        with open(settings.PYTHON_SCRIPT_TEST_RESULTS_PATH, 'r') as file:
            data = json.load(file)
    except FileNotFoundError:
        data = {}  # Initialize to an empty dictionary if file doesn't exist
    except json.JSONDecodeError:
        raise ValueError("Error parsing JSON file")

    # Check if the code_key exists
    if code_key not in data:
        raise ValueError(f"Key '{code_key}' not found in JSON file")

    # Determine which testing type to update
    testing_type = "autonomous_testing" if autonomous_on else "manual_testing"

    # Update the success data
    if testing_type in data[code_key]:
        data[code_key][testing_type]['success'] = success_data
    else:
        raise ValueError(f"Testing type '{testing_type}' not found for key '{code_key}'")

    # Save the updated data back to the file
    with open(settings.PYTHON_SCRIPT_TEST_RESULTS_PATH, 'w') as file:
        json.dump(data, file, indent=4)