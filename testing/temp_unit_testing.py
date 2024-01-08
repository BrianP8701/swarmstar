import json
import asyncio
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from swarm.settings import Settings

from swarm.core.memory.testing_ground.python_scripts.schema import python_script_test_result_template
from swarm.core.swarm import Swarm
import traceback
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
                if d[k] is None:  # Check if the current value of d[k] is None
                    d[k] = {}  # Initialize it as an empty dictionary
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
    save_progress(code_key, {'autonomous_testing': {'synthetic_executable_script_for_testing': script_assessment['arguments']}})
    return script_assessment

script_message = (
    f'<CODE STARTS>\nprint(\'Hello World\')\n<CODE ENDS>\n'
    f'<DESCRIPTION STARTS>\nA simple script that prints \'Hello World\' to the console.\n<DESCRIPTION ENDS>\n'
)
snapshot_path = 'tool_building/past_runs/v6/snapshot.json'
history_path = 'tool_building/past_runs/v6/history.json'

swarm = Swarm(snapshot_path, history_path)

async def generate_test_script(code_key, script_assessment, script_message, code, swarm):
    script_message += f'\nCode key to use in update_python_script_test_success: {code_key}\n'
    executable_python_test_script_generator = swarm.agents['python_test_script_generator']
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

    executable_script = await executable_python_test_script_generator.chat(script_message)
    save_progress(code_key, {'autonomous_testing': {'synthetic_executable_script_for_testing': executable_script['arguments']}})
    return executable_script



assessment = {'function_name': 'plan_script_test', 'arguments': {'is_script_runnable_as_is': True, 'needs_user_provided_parameters': False}}
generated_script = {'function_name': 'make_script_executable', 'arguments': {'executable_script': "import json\nfrom swarm.utils import update_python_script_test_success\n\ndef main():\n    output = 'Hello World'\n    print(output)\n    \n    success_message = {\n        'input': {},\n        'output': {'message': output}\n    }\n    update_python_script_test_success('hello_world', True, success_message)\n\nif __name__ == '__main__':\n    main()\n"}}
async def try_executing_synthetic_script(code_key, executable_script):
    try: 
        print('\n\nAHHHHHHHHHHHH')
        print(executable_script['arguments']['executable_script'])
        try:
            exec(executable_script['arguments']['executable_script'])  
        except Exception as e:
            print(f'\n\nError executing script {code_key}: {e}')
            traceback.print_exc()
            raise e
        print('\n\nAHHHHHHHHHHHH')
    except Exception as e:
        error_message = f"Error executing script {code_key}: {e}"
        save_progress(code_key, {'autonomous_testing': {'error': error_message}})
        raise Exception(error_message)
    
    
async def main():
    
    # generated_script = await generate_test_script('hello_world', assessment, script_message, 'print(\'Hello World\')', swarm)
    # print(generated_script)
    await try_executing_synthetic_script('hello_world', generated_script)

# Run the main function
asyncio.run(main())