'''
Temporary file to write and add functions to the functions.json file manually. Write your function starting from line 40
'''

import json
from settings import Settings

settings = Settings()

def save_python_file_to_json(file_path, json_path, name, description, start_line):
    """
    Save a Python file to a JSON file with an additional description.

    :param file_path: Path to the Python file.
    :param json_path: Path to the JSON file.
    :param name: The key to add to the JSON dictionary.
    :param description: The description to add under the key.
    :param start_line: The line number from which to start reading the Python file.
    """
    # Read the Python file from a specific line number to the end
    try:
        with open(file_path, 'r') as file:
            # Skip lines until the start_line
            for _ in range(start_line - 1):
                next(file)
            file_content = file.read()
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

    # Update the dictionary with the new key-value pair
    data[name] = {
        'code': file_content,
        'description': description
    }

    # Write the updated dictionary back to the JSON file
    try:
        with open(json_path, 'w') as json_file:
            json.dump(data, json_file, indent=4)
    except IOError as e:
        print(f"Error writing to JSON file {json_path}: {e}")

description = "Routes a task to the appropriate next action.\n\tInput: A list of subtasks (list), a string describing the context of the goal (str), and a boolean indicating whether the subtasks should be executed in parallel or sequentially (bool)\n\tReturns: None\nCalls the subtask_router_agent to route a subtask to the appropriate next action. Schedules tasks in swarm correspondingly:\nA dictionary with the following keys:\n\t'next_action': An integer indicating the next action to take (1: break_down_goal, 2: write_text, 3: write_python, 4: retrieve_info, 5: ask_user_for_help)"
save_python_file_to_json('tool_building/write_functions.py', settings.FUNCTIONS_PATH, 'route_task', description, 56)

# Write function below: 
from swarm.swarm import Swarm
from task import Task
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