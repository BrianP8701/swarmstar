'''
Write and add scripts to node_scripts.json
'''

# <-- Script start -->
from swarm.swarm import Swarm
async def route_task(subtasks, context, is_parallel):
    swarm = Swarm()
    router_agent = swarm.agents['router_agent']
    task_list = ['break_down_goal', 'write_text', 'write_python', 'retrieve_info', 'ask_user_for_help']
    save_message = {}
    
    def route_to_task_from_action_index(action_index, subtask):
        goal = {'goal': f'Context to understand the task: {context}\n\n\n The task: {subtask}'}
        next_task = Task(task_list[action_index], goal)
        swarm.task_queue.put_nowait(next_task)
        save_message[subtask] = task_list[action_index]
        
    def messagify(subtask):
        return f"Context to understand the task: {context}\n\n\n The task. Decide what we should do next to accomplish this: {subtask}"
    
    if not is_parallel:
        action_index = await router_agent.chat(messagify(subtasks[0]))
        action_index = action_index['arguments']['next_action']
        route_to_task_from_action_index(action_index-1, subtasks[0])
    else:
        for subtask in subtasks:
            action_index = await router_agent.chat(messagify(subtask))
            action_index = action_index['arguments']['next_action']
            route_to_task_from_action_index(action_index-1, subtask)
            
    swarm.save(swarm.save_path, save_message)
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

save_python_file_to_json('tool_building/write_functions.py', settings.NODE_SCRIPTS_PATH, 'route')