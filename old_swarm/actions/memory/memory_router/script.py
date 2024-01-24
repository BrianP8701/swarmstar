import json
import copy
import sys
import asyncio
import os
import shutil
sys.path.insert(0, '/Users/brianprzezdziecki/Code/Agent_Swarm_Experiments')

from old_swarm.core.oai_agent import OAI_Agent
from old_swarm.settings import Settings
from old_swarm.utils.actions.validate_action_args import validate_action_args
from old_swarm.utils.actions.executor import execute_script
from old_swarm.utils.memory.firestore_wrapper import save_dict_to_firestore
settings = Settings()

async def memory_router(data_id: str):
    '''
    The memory router finds where to save a piece of data
    '''
    with open('swarm/actions/memory/memory_router/tool.json') as f:
        router_schema = json.load(f)
    tool_blueprint = router_schema['memory_router']['tools'][0]
    instructions = router_schema['memory_router']['instructions']
    
    metadata_path = f'swarm/stage/_meta_{data_id}.json'
    with open(metadata_path) as f:
        metadata = json.load(f)

    memory_space_path = 'swarm/memory'
        
    searching_memory_space = True
    options = _extract_options(memory_space_path)
    description = 'This is the root of the memory space.'
    path = ['swarm', 'memory']

    while searching_memory_space:
        # Let LLM choose where to go in the action_space
        tool_blueprint_copy = copy.deepcopy(tool_blueprint)
        memory_router = _update_router(options, tool_blueprint_copy, instructions, description)
        memory_router_output = await memory_router.chat(f'This is the metadata of the file to save:\n{str(metadata)}')
        folder_index = memory_router_output['arguments'].get('folder_index', None)
        
        # Get assistance from the user if needed
        stop = memory_router_output['arguments'].get('stop', False)
        if stop or folder_index == None: break

        # Continue to traverse action space if you are in a folder. Exit if you are in an action.
        path.append(options[folder_index]['name'])
        
        node_info_path = os.path.join(*path, '_node_info.json')
        try:
            with open(node_info_path, 'r') as json_file:
                node_info = json.load(json_file)
        except FileNotFoundError:
            print(f"File {node_info_path} does not exist.")
            node_info = None

        if node_info['type'] == 'folder':
            options = _extract_options(os.path.join(*path))
            if len(options) == 0:
                searching_memory_space = False
        elif node_info['type'] == 'special':
            # TODO TODO TODO TODO TODO 
            pass
        else:
            raise ValueError(f"Invalid type in memory space. Expected 'folder' or 'special'.\n\nPath: {path}\n\n")
    
    # Move file to new destination
    source_path = f'swarm/stage/{data_id}.{metadata["file_extension"]}'
    destination_path = os.path.join(*path, f'{data_id}.{metadata["file_extension"]}')
    shutil.move(source_path, os.path.join(*path))
    # Move metadata to firestore
    save_dict_to_firestore('memory_metadata', destination_path.replace('/', '-'), metadata)
    os.remove(metadata_path)
    
    lifecycle_command = {'action': 'terminate', 'node_blueprints': []}
    report = {
        'message': f'Given the data_id "{data_id}", the memory router chose the folder "{"/".join(path)}"',
        'folder_path': "/".join(path)
    }
    return {'report': report, 'lifecycle_command': lifecycle_command}

def _update_router(options, tool, instructions, description):
    tool['function']['parameters']['properties']['folder_index']['description'] += f'\n\nDescription of current folder: {description}\n\nOptions:'
    tool['function']['parameters']['properties']['folder_index']['description'] += str(options)
    tool['function']['parameters']['properties']['folder_index']['enum'] = list(range(len(options)))

    tool_choice = {"type": "function", "function": {"name": "memory_router"}}
    
    return OAI_Agent(instructions, [tool], tool_choice)

def _extract_options(base_folder):
    """
    Scans the subfolders in the base_folder for _node_info.json files,
    and returns a dict with incrementing indices as keys and the content
    of these json files as values.

    :param base_folder: The path of the folder to scan.
    :return: Dict of indices to json content.
    """
    node_info_dict = {}
    index = 0

    for folder in os.listdir(base_folder):
        json_path = os.path.join(base_folder, folder, '_node_info.json')
        if os.path.isfile(json_path):
            with open(json_path, 'r') as json_file:
                node_info_dict[index] = json.load(json_file)
                index += 1

    return node_info_dict

def main(args):
    try:
        results = asyncio.run(memory_router(args['data_id']))
        print(json.dumps(results))  # Convert dict to JSON and print
    except Exception as e:
        raise RuntimeError(f"Script execution failed: {str(e)}")

if __name__ == "__main__":
    schema = {
        "data_id": str
    }
    args_dict = validate_action_args(schema)
    main(args_dict)