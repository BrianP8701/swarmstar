import json

def save_python_file_to_json(file_path, json_path, key):
    # Read the Python file and convert it to a string
    try:
        with open(file_path, 'r') as file:
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

save_python_file_to_json('temppp.py', 'tool_building/config/functions.json', 'route_subtasks')

from swarm.swarm import Swarm
from task import Task
async def break_down_goal(goal):
    swarm = Swarm()
    broken_down_goal = await swarm.agents['head_agent'].chat(goal)
    next_task = Task('route_subtasks', broken_down_goal['arguments'])
    swarm.task_queue.put_nowait(next_task)


from swarm.swarm import Swarm
async def route_subtasks(broken_down_goal):
    swarm = Swarm()
    subtasks = broken_down_goal['subtasks']
    is_parallel = broken_down_goal['is_parallel']
    context = broken_down_goal['context']
    task_list = ['break_down_goal', 'write_python', 'retrieve_info', 'ask_user_for_help']
    
    def route_to_task_from_action_index(action_index, subtask):
        data = {'task': subtask, 'context': context}
        next_task = Task(task_list[action_index], data)
        swarm.task_queue.put_nowait(next_task)
        
    def messagify(subtask):
        return f"Context to understand the task: {context}\n\n\n The task. Decide what we should do next to accomplish this: {subtask}"
    
    if not is_parallel:
        action_index = await swarm.agents['subtask_router_agent'].chat(messagify(subtasks[0]))['arguments']['action_index']
        route_to_task_from_action_index(action_index-1, subtasks[0])
    else:
        for subtask in subtasks:
            action_index = await swarm.agents['subtask_router_agent'].chat(messagify(subtask))['arguments']['action_index']
            route_to_task_from_action_index(action_index-1, subtask)