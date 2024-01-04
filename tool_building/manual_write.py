'''
Write and add scripts to node_scripts.json
'''

# <-- Script start -->
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
    code_type = ['function', 'class', 'script', 'other']
    packet = {
        'language': 'python',
        'code_type': code_type[code['arguments']['code_type']],
        'code': code['arguments']['python_code'],
        'description': code['arguments']['description'],
        'dependencies': code['arguments']['dependencies']
    }

    file_name = settings.SYNTHETIC_CODE_PATH
    with open(file_name, 'r') as file:
        data = json.load(file)
    data[code['arguments']['name']] = packet
    with open(file_name, 'w') as file:
        json.dump(data, file, indent=4)

    return {'action': 'terminate', 'node_blueprints': []}    
# <-- Script end -->




import json
from settings import Settings

settings = Settings()

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

save_python_file_to_json('tool_building/manual_write.py', settings.NODE_SCRIPTS_PATH, 'python_coder')