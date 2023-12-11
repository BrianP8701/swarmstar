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

save_python_file_to_json('tool_building/write_functions.py', 'tool_building/config/functions.json', 'write_python', 40)

# Write function below:
from swarm.swarm import Swarm
from swarm.agent import Agent
from task import Task
async def write_python(goal):
    print(f'\n\n{goal}\n\n')
    swarm = Swarm()
    python_agent: Agent = swarm.agents['write_python_agent']
    
    tool_output = await python_agent.chat(goal)
    print('bitch ass md here')
    print(f'\n\n{tool_output}\n\n')
    python_code = tool_output['arguments']['python_code']
    
    next_task = Task('save_python_code', tool_output['arguments'])
    swarm.task_queue.put_nowait(next_task)
    save_message = f'The code we wrote to solve: {goal} \n\n{python_code}'
    swarm.save(swarm.save_path, save_message)