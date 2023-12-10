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

save_python_file_to_json('tool_building/swarm/write_functions.py', 'tool_building/config/functions.json', 'write_python', 40)

# Write function below:
from swarm.swarm import Swarm
from swarm.agent import Agent
import json
async def write_python(goal):
    swarm = Swarm()
    task_handler = swarm.task_handler
    python_agent: Agent = swarm.agents['write_python_agent']
    python_test_cases_agent: Agent = swarm.agents['python_test_cases_agent']
    
    tool_output = await python_agent.chat(goal)
    python_code = tool_output['arguments']['python_code']
    
    test_cases = 
    
    # Create test cases for function
    with open('tool_building/config/test_cases.json', 'r') as file:
        test_cases = json.load(file)