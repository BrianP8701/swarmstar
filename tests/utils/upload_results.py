import os
import json

def create_result_file():
    '''
    During testing we can store each swarm operation sequentially to better debug the swarm.
    
    This file will simply create a new file in the tests/results directory with the name "swarm_run_{x}.json" where x is the next available number.
    
    You can clear this folder out at any time to start fresh.
    '''
    x = 0
    while True:
        file_name = f"tests/results/swarm_run_{x}.json"
        if not os.path.exists(file_name):
            with open(file_name, 'w') as file:
                json.dump([], file)
            print(f"Result file created: {file_name}")
            return file_name
        x += 1

def add_swarm_operation(file_name, swarm_operation):
    '''
    Add a swarm operation to the result file.
    '''
    with open(file_name, 'r') as file:
        data = json.load(file)
    
    data.append(swarm_operation.model_dump_json(indent=4))
    with open(file_name, 'w') as file:
        json.dump(data, file)