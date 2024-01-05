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
        question = broken_down_goal['arguments']['question']

        if agent_has_questions:
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

    
    