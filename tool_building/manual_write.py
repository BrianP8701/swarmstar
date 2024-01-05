'''
Write and add scripts to node_scripts.json
'''

# <-- Script start -->
from settings import Settings
import json
from swarm.swarm import Swarm
import os

settings = Settings()
with open(settings.AUTONOMOUS_SCRIPT_TESTS_PATH, 'r') as file:
    autonomous_test_data = json.load(file)
    
# DO same but with manualk
with open(settings.MANUAL_SCRIPT_TESTS_PATH, 'r') as file:
    manual_test_data = json.load(file)
    
def save_test_progress(data, code_key, inner_key, value):
    if code_key not in data:
        data[code_key] = {} 
    if inner_key not in data[code_key]:
        data[code_key][inner_key] = {} 
    data[code_key][inner_key] = value
    with open(settings.AUTONOMOUS_SCRIPT_TESTS_PATH, 'w') as file:
        json.dump(data, file, indent=4)
        
async def python_script_tester(code_key):
    swarm = Swarm()
    with open(settings.SYNTHETIC_CODE_PATH, 'r') as file:
        data = json.load(file)
    synthetic_code_bundle = data[code_key]
    code = synthetic_code_bundle['code']
    description = synthetic_code_bundle['description']
    save_test_progress(autonomous_test_data, code_key, 'original_script', code)
    
    try:
        # Assess the script
        python_script_assessor_pre_testing = swarm.agents['python_script_assessor_pre_testing']
        script_assessment = await python_script_assessor_pre_testing.chat(f'<CODE STARTS>\n{code}\n<CODE ENDS>\n{description}')
        save_test_progress(autonomous_test_data, code_key, 'script_assessment', script_assessment['arguments'])
        
        # Generate a script to test the script
        message_to_generate_proper_script = f'<CODE STARTS>\n{code}\n<CODE ENDS>\n<DESCRIPTION>\n{description}\n<DESCRIPTION ENDS>\n'
        if script_assessment['arguments']['is_script_runnable_as_is']:
            message_to_generate_proper_script += '\n<Script is runnable as is.>\n'
        else:
            message_to_generate_proper_script += '\n<Script is not runnable as is. You need to leave the script unchanged, adding logic to execute and fill in blank parameters as necessary.>\n'
            if script_assessment['arguments'].get('needs_user_provided_parameters', False):
                user_input = input(f"\n\nThe python script tester needs you to provide input parameters to test this script: \n{code}\n\nPlease provide the name of the parameters followed by the value.")
                message_to_generate_proper_script += f'<USER PARAMS>\n{user_input}\n<USER PARAMS ENDS>\n'
        message_to_generate_proper_script += f"\n**Success Logging Params**:\nJSON_SAVE_SUCCESS_PATH = '{settings.AUTONOMOUS_SCRIPT_TESTS_PATH}'\nSCRIPT_KEY = '{code_key}'"
        executable_python_test_script_generator = swarm.agents['executable_python_test_script_generator']
        executable_script = await executable_python_test_script_generator.chat(message_to_generate_proper_script)
        save_test_progress(autonomous_test_data, code_key, 'synthetic_executable_script_for_testing', executable_script['arguments']['executable_script'])
        
        # Execute the script that tests the script
        try: 
            exec(executable_script['arguments']['executable_script'])  
        except Exception as e:
            error_message = f"Error executing script {code_key}: {e}"
            save_test_progress(autonomous_test_data, code_key, 'error', error_message)
            raise Exception(error_message)
    except: # If the autonomous testing fails at any point, we need to manually prepare the script for testing
        manual_test_file_path = f'{settings.MANUAL_TESTING_GROUND_FOLDER_PATH}/{code_key}.py'
        save_test_progress(manual_test_data, code_key, 'original_script', code)
        if not os.path.exists(manual_test_file_path):
            open(manual_test_file_path, 'w').close()
        with open(manual_test_file_path, 'w') as file:
            file.write(code)
        user_input = input(f'\nThe autonomous script tester failed. Please manually prepare the script for testing at {manual_test_file_path} and press enter when ready.\nAdd logic to save the result of the successful test in {settings.MANUAL_SCRIPT_TESTS_PATH} file as follows:\nPrepare a success message that includes two dictionaries:\n- input: Containing the parameters used for the test.\n- output: Detailing the results or outputs from the test execution.\nThese will be added to a JSON file so make sure they are serializable. Leave out non-serializable data.\nSave the success dict to the file: {settings.MANUAL_SCRIPT_TESTS_PATH} with the key: {code_key}\n\nPress enter when ready.\n')
        
        try:
            with open(manual_test_file_path, 'r') as file:
                manually_prepared_test_script = file.read()
                save_test_progress(manual_test_data, code_key, 'manually_prepared_test_script', manually_prepared_test_script)
                exec(manually_prepared_test_script)
        except Exception as e:
            error_message = f"Error executing script {code_key}: {e}"
            save_test_progress(manual_test_data, code_key, 'error', error_message)
            raise Exception(error_message)
        
    return {'action': 'terminate', 'node_blueprints': []}
    # Ok. so now we should have a success message in the autonomous or manual test data, or an error message in the autonomous test data. what do we do now?

    
    
# <-- Script end -->






def save_python_file_to_json(file_path, json_path, name, description=None, language=None):
    """
    Save a portion of a Python file to a JSON file. The portion is defined between 
    '# <-- Script start -->' and '# <-- Script end -->' flags in the file. 
    If 'description' or 'language' are not provided, existing values are retained in the JSON.

    :param file_path: Path to the Python file.
    :param json_path: Path to the JSON file.
    :param name: The key to add to the JSON dictionary.
    :param description: (Optional) Description for the script.
    :param language: (Optional) Programming language of the script.
    """
    # Read the Python file and extract content between the flags
    try:
        with open(file_path, 'r') as file:
            recording = False
            file_content = ''
            for line in file:
                if '# <-- Script end -->' in line:
                    break
                if recording:
                    file_content += line
                if '# <-- Script start -->' in line:
                    recording = True
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

    # Update the dictionary with the new content
    if name not in data:
        data[name] = {'script': '', 'description': '', 'language': ''}

    data[name]['script'] = file_content
    if description is not None:
        data[name]['description'] = description
    if language is not None:
        data[name]['language'] = language

    # Write the updated dictionary back to the JSON file
    try:
        with open(json_path, 'w') as json_file:
            json.dump(data, json_file, indent=4)
    except IOError as e:
        print(f"Error writing to JSON file {json_path}: {e}")

save_python_file_to_json('tool_building/manual_write.py', settings.NODE_SCRIPTS_PATH, 'python_script_tester')