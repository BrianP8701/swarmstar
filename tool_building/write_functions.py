'''
Temporary file to write and add functions to the functions.json file manually. Write your function starting from line 40
'''

import json

def save_python_file_to_json(file_path, json_path, key, start_line):
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
    data[key] = file_content

    # Write the updated dictionary back to the JSON file
    try:
        with open(json_path, 'w') as json_file:
            json.dump(data, json_file, indent=4)
    except IOError as e:
        print(f"Error writing to JSON file {json_path}: {e}")

save_python_file_to_json('tool_building/write_functions.py', 'tool_building/config/functions.json', 'route_task', 40)

# Write function below:
from swarm.swarm import Swarm
from task import Task
async def route_task(subtasks, context, is_parallel):
    swarm = Swarm()
    task_list = ['break_down_goal', 'write_text', 'write_python', 'retrieve_info', 'ask_user_for_help']
    
    def route_to_task_from_action_index(action_index, subtask):
        data = {'context': context, 'task': subtask}
        next_task = Task(task_list[action_index], data)
        swarm.task_queue.put_nowait(next_task)
        save_message = f'We will call {task_list[action_index]} to accomplish: {subtask}'
        swarm.save(swarm.save_path, save_message)
        
    def messagify(subtask):
        return f"Context to understand the task: {context}\n\n\n The task. Decide what we should do next to accomplish this: {subtask}"
    
    if not is_parallel:
        action_index = await swarm.agents['subtask_router_agent'].chat(messagify(subtasks[0]))
        action_index = action_index['arguments']['next_action']
        route_to_task_from_action_index(action_index-1, subtasks[0])
    else:
        for subtask in subtasks:
            action_index = await swarm.agents['router_agent'].chat(messagify(subtask))
            action_index = action_index['arguments']['next_action']
            route_to_task_from_action_index(action_index-1, subtask)