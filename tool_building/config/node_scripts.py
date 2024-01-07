'''
Every script should output a dictionary with one of the following structure:
{
    'action': 'create children' or 'terminate',
    'node_blueprints': list of node blueprints to be created
}   
'''

'''
+----------------- manager -----------------+
'''
from swarm.swarm import Swarm
async def manager(goal):
    swarm = Swarm()
    manager = swarm.agents['manager']
    
    while True:
        broken_down_goal = await manager.chat(goal)
        agent_has_questions = broken_down_goal['arguments']['do_you_have_questions']

        if agent_has_questions:
            question = broken_down_goal['arguments']['question']
            user_input = input(f"Questions: {question}\n\nGoal: {goal}\n\n")
            goal = f'{goal}\n\nQuestion: {question} \n\nUser answer: {user_input}'
        else:
            subgoals = broken_down_goal['arguments']['subgoals']
            break
            
    node_blueprints = []
    for subgoal in subgoals:
        node_blueprints.append({'type': 'router', 'data': {'goal': subgoal}})

    return {'action': 'spawn', 'node_blueprints': node_blueprints}
'''
+----------------- router -----------------+
'''
from swarm.swarm import Swarm
async def router(goal):
    swarm = Swarm()
    router_agent = swarm.agents['router']
    options = ['user_assistance', 'python_coder', 'manager', 'writer', 'retrieval']
    
    agent_index = await router_agent.chat(goal)
    agent_index = agent_index['arguments']['agent_index']
    
    if agent_index == 0: # User assistance
        while True:
            user_input = input(f"The router agent needs assistance routing this goal:\n\n{goal}\n\nPlease choose the index of the agent this goal should be routed to: {options}")
            if user_input.isdigit():
                user_number = int(user_input)
                if 1 <= user_number <= len(options):
                    print(f"You chose the number: {user_number}")
                    agent_index = user_number
                    break
                else:
                    print("Number out of range. Please try again. Don't select user_assistance again.")
            else:
                print("Invalid input. Please enter a number.")
                
    node_blueprints = [{'type': options[agent_index], 'data': {'goal': goal}}]
    return {'action': 'spawn', 'node_blueprints': node_blueprints}

'''
+----------------- python_coder -----------------+
'''
from swarm.swarm import Swarm
from settings import Settings
import json
settings = Settings() # For config paths

async def python_coder(goal):
    swarm = Swarm()
    
    # Gather all relevant context
    code_analyst = swarm.agents['code_analyst']
    while True:
        questions = await code_analyst.chat(goal)
        analyst_has_questions = questions['arguments']['do_you_have_questions']
        
        if analyst_has_questions:
            questions = questions['arguments']['questions']
            user_input = input(f"\n\nGoal: {goal}\n\nQuestions: {questions}\n")
            goal = f'{goal}\n\nQuestions: {questions} \n\nUser answer: {user_input}'
        else: 
            break

    # Write code
    python_coder = swarm.agents['python_coder']
    code = await python_coder.chat(goal)
    code = code['arguments']['python_code']
    python_metadata_extractor = swarm.agents['python_metadata_extractor']
    metadata = await python_metadata_extractor.chat(code)
    name = metadata['arguments']['name']
    code_type = ['function', 'class', 'script', 'other']
    packet = {
        'language': 'python',
        'code_type': code_type[metadata['arguments']['code_type']],
        'code': code,
        'description': metadata['arguments']['description'],
        'dependencies': metadata['arguments'].get('dependencies', [])
    }

    file_name = settings.SYNTHETIC_CODE_PATH
    with open(file_name, 'r') as file:
        data = json.load(file)
    data[name] = packet
    with open(file_name, 'w') as file:
        json.dump(data, file, indent=4)

    node_blueprints = [{'type': 'python_script_tester', 'data': {'code_key': name}}]
    return {'action': 'spawn', 'node_blueprints': node_blueprints}    

'''
+----------------- python_script_tester -----------------+
'''
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

async def manually_prepare_script_for_testing(code_key, code, script_message):
    manual_test_file_path = f'{settings.MANUAL_PATH}/{code_key}.py'
    save_progress(code_key, {'manual_testing': {'manual_test_file_path': manual_test_file_path}})
    if not os.path.exists(manual_test_file_path):
        open(manual_test_file_path, 'w').close()
    with open(manual_test_file_path, 'w') as file:
        file.write(code)
    await async_input(
        f'\nThe autonomous script tester failed. Please add logic to execute the code in '
        f'{manual_test_file_path}.\n\n'
        f'Prepare a success message that includes two dictionaries:\n'
        f'  - input: Containing the parameters used for the test.\n'
        f'  - output: Detailing the results or outputs from the test execution.\n'
        f'\nTo save the success message:\n'
        f'from swarm.utils import update_python_script_test_success\n\n'
        f'When the success message is ready:\n'
        f'update_python_script_test_success({code_key}, {False}, your_success_message)\n'
        f'\n'
        f'Press enter when ready.\n'
    )
    return

async def try_executing_manually_prepared_script(code_key):
    try:
        with open(f'{settings.MANUAL_PATH}/{code_key}.py', 'r') as file:
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
        await manually_prepare_script_for_testing(code_key, code, script_message)
        await try_executing_manually_prepared_script(code_key)

    return {'action': 'terminate', 'node_blueprints': []}