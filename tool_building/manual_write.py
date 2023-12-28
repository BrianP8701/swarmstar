'''
Write and add scripts to node_scripts.json
'''

# <-- Script start -->
from swarm.swarm import Swarm
async def break_down_goal(goal, context):
    swarm = Swarm()
    manager = swarm.agents['manager']
    broken_down_goal = await manager.chat(f'Context to understand the goal: {context}\n\n\n The goal: {goal}')

    node_blueprints = []
    for subgoal in broken_down_goal['arguments']['subtasks']:
        node_blueprints.append({'type': 'router', 'data': subgoal})
        if broken_down_goal['arguments']['is_parallel']:
            break
    return {'action': 'create children', 'node_blueprints': node_blueprints}
# <-- Script end -->




from swarm.swarm import Swarm
from swarm.agent import Agent
async def write_python(goal):
    swarm = Swarm()
    python_agent: Agent = swarm.agents['write_python_agent']
    
    tool_output = await python_agent.chat(goal)
    code_type = tool_output['arguments']['code_type']
    python_code = tool_output['arguments']['python_code']
    name = tool_output['arguments']['name']
    description = tool_output['arguments']['description']
    
    # TODO TODO TODO TODO TODO TODO WE ARE WORKING HERE!!!!! TODO TODO TODO TODO TODO TODO
    # save python code, then idk.....







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

save_python_file_to_json('tool_building/manual_write.py', settings.NODE_SCRIPTS_PATH, 'manager')