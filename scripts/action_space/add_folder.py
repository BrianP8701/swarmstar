import os
from dotenv import load_dotenv
import json

from swarm_star.utils.ai.openai_instructor import completion
from swarm_star.swarm.types import ActionMetadata

load_dotenv() # Load environment variables from .env file

openai_key = os.getenv('OPENAI_KEY')
if not openai_key:
    raise ValueError("OPENAI_KEY not found in .env file.")

def manual_add_folder_to_action_space(folder_path: str, description: str):
    # Ensure the script_path is relative to 'swarm_star/actions' and format it accordingly
    base_path = 'swarm_star/actions'
    if folder_path == base_path:
        raise ValueError(f"The folder must be within the '{base_path}' directory.")
    if base_path not in folder_path:
        raise ValueError(f"The folder must be within the '{base_path}' directory.")
    # Extract the relative path from the full folder_path
    relative_path_index = folder_path.index(base_path)
    folder_path = folder_path[relative_path_index:].strip('/')
    # Get the parent folder of the script, ensuring it does not start or end with '/'
    parent_path = '/'.join(folder_path.split('/')[:-1]).strip('/')

    print(f'folder_path: {folder_path}')
    print(f'parent_id: {parent_path}')
    name = os.path.splitext(os.path.basename(folder_path))[0]
    print(name)
    
    action_metadata = ActionMetadata(
        is_folder=True,
        type='internal_folder',
        name=os.path.splitext(os.path.basename(folder_path))[0],
        description=description,
        parent=parent_path,
        children=[],
        metadata={
            "script_path": folder_path.replace('/', '.').rsplit('.', 1)[0]
        }
    )
    
    action_metadata = action_metadata.model_dump()
    with open('swarm_star/actions/action_space.json', 'r+') as file:
        data = json.load(file)
        data[folder_path] = action_metadata
        data[parent_path]['children'].append(folder_path)
        file.seek(0)
        json.dump(data, file)
        file.truncate()
    
description = 'Contains actions to interact with the user'
manual_add_folder_to_action_space('swarm_star/actions/communication', description)
