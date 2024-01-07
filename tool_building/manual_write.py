'''
Write and add scripts to node_scripts.json
'''

# <-- Script start -->
from settings import Settings
import json
from swarm.swarm import Swarm
import os
from swarm.memory.testing_ground.python_scripts.schema import python_script_test_result_template
import asyncio

settings = Settings()

def load_json_data(path):
    with open(path, 'r') as file:
        return json.load(file)
      
def save_progress(code_key, updates):
    try:
        data = load_json_data(settings.PYTHON_SCRIPT_TEST_RESULTS_PATH)
    except (FileNotFoundError, json.JSONDecodeError):
        data = {}

    # If code_key is new, initialize it using the template
    if code_key not in data:
        data[code_key] = python_script_test_result_template.copy()

    # Recursive function to update the dictionary
    def update_dict(d, u):
        for k, v in u.items():
            if isinstance(v, dict):
                d[k] = update_dict(d.get(k, {}), v)
            else:
                d[k] = v
        return d

    # Update the data
    data[code_key] = update_dict(data[code_key], updates)

    # Save the updated data back to the file
    with open(settings.PYTHON_SCRIPT_TEST_RESULTS_PATH, 'w') as file:
        json.dump(data, file, indent=4)
        
async def async_input(prompt: str = "") -> str:
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(None, input, prompt)

async def assess_script(code_key, script_message, swarm):
    python_script_assessor_pre_testing = swarm.agents['python_script_assessor_pre_testing']
    script_assessment = await python_script_assessor_pre_testing.chat(script_message)
    save_progress(code_key, {'autonomous_testing': {'script_assessment': script_assessment['arguments']}})
    return script_assessment

async def generate_test_script(code_key, script_assessment, script_message, code, swarm):
    executable_python_test_script_generator = swarm.agents['executable_python_test_script_generator']
    if script_assessment['arguments']['is_script_runnable_as_is']:
        script_message += '\n<Script is runnable as is.>\n'
    else: 
        script_message += (
            '\n<Script is not runnable as is. You need to leave the script unchanged, '
            'adding logic to execute and fill in blank parameters as necessary.>\n'
        )
        if script_assessment['arguments'].get('needs_user_provided_parameters', False):
            user_input = await async_input(
                "\n\nThe python script tester needs you to provide input parameters to test this script: "
                f"\n{code}\n\nPlease provide the name of the parameters followed by the value."
            )
            script_message += f'<USER PARAMS>\n{user_input}\n<USER PARAMS ENDS>\n'
    script_message += (
        f"\n**Success Logging Params**:\n"
        f"JSON_SAVE_SUCCESS_PATH = '{settings.AUTONOMOUS_SCRIPT_TESTS_PATH}'\n"
        f"SCRIPT_KEY = '{code_key}'"
    )
    executable_script = await executable_python_test_script_generator.chat(script_message)
    save_progress(code_key, {'autonomous_testing': {'executable_script': executable_script['arguments']}})
    return executable_script

async def try_executing_synthetic_script(code_key, executable_script):
    try: 
        exec(executable_script['arguments']['executable_script'])  
    except Exception as e:
        error_message = f"Error executing script {code_key}: {e}"
        save_progress(code_key, {'autonomous_testing': {'error': error_message}})
        raise Exception(error_message)

async def manually_prepare_script_for_testing(code_key, script_message):
    manual_test_file_path = f'{settings.MANUAL_PATH}/{code_key}.py'
    save_progress(code_key, {'manual_testing': {'manual_test_file_path': manual_test_file_path}})
    if not os.path.exists(manual_test_file_path):
        open(manual_test_file_path, 'w').close()
    with open(manual_test_file_path, 'w') as file:
        file.write(script_message)
    await async_input(
        f'\nThe autonomous script tester failed. Please manually prepare the script for testing at {manual_test_file_path} '
        f'and press enter when ready.\nAdd logic to save the result of the successful test in {settings.MANUAL_SCRIPT_TESTS_PATH} file as follows:\n'
        f'Prepare a success message that includes two dictionaries:\n'
        f'- input: Containing the parameters used for the test.\n'
        f'- output: Detailing the results or outputs from the test execution.\n'
        f'These will be added to a JSON file so make sure they are serializable. Leave out non-serializable data.\n'
        f'Save the success dict to the file: {settings.MANUAL_SCRIPT_TESTS_PATH} with the key: {code_key}\n\n'
        f'Press enter when ready.\n'
    )
    return

async def try_executing_manually_prepared_script(code_key):
    try:
        with open(f'{settings.MANUAL_TESTING_GROUND_FOLDER_PATH}/{code_key}.py', 'r') as file:
            manually_prepared_test_script = file.read()
            save_progress(code_key, {'manual_testing': {'manually_prepared_test_script': manually_prepared_test_script}})
            exec(manually_prepared_test_script)
    except Exception as e:
        error_message = f"Error executing script {code_key}: {e}"
        save_progress(code_key, {'manual_testing': {'error': error_message}})
        raise Exception(error_message)

async def python_script_tester(code_key):  
    swarm = Swarm()
    # Load the script to be tested
    synthetic_code_database = load_json_data(settings.SYNTHETIC_CODE_PATH)
    code = synthetic_code_database[code_key]['code']
    script_message = (
        f'<CODE STARTS>\n{synthetic_code_database[code_key]["code"]}\n<CODE ENDS>\n'
        f'<DESCRIPTION STARTS>\n{synthetic_code_database[code_key]["description"]}\n<DESCRIPTION ENDS>\n'
    )
    save_progress(code_key, {'original_script': script_message})

    try: # autonomously preparing and testing the script
        script_assessment = await assess_script(code_key, script_message, swarm)
        executable_script = await generate_test_script(code_key, script_assessment, script_message, code, swarm)
        await try_executing_synthetic_script(executable_script)
    except: # manually prepare and test the script
        manually_prepare_script_for_testing(code_key, script_message)
        await try_executing_manually_prepared_script(code_key)

    return {'action': 'terminate', 'node_blueprints': []}
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