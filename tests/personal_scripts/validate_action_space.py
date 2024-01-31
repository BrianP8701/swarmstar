import json



import os
from pydantic import BaseModel, ValidationError
from typing import Dict, List, Optional
from aga_swarm.swarm.types import *

# Function to validate the ASM dict
def validate_asm(asm: Dict[str, ActionMetadata]):
    for key, value in asm.items():
        # Check if type exists
        if 'type' not in value:
            print(f"{key} does not have a type")
            continue
        
        # Check if it's a folder or file
        if value['type'] == 'folder':
            if not os.path.isdir(key):
                print(f"{key} does not exist as a folder")
            try:
                ActionFolderMetadata(**value)
            except ValidationError as e:
                print(f"{key} does not follow schema: {e}")
                
        elif value['type'] == 'file':
            if not os.path.isfile(key):
                print(f"{key} does not exist as a file")
            try:
                ActionMetadata(**value)
            except ValidationError as e:
                print(f"{key} does not follow schema: {e}")

        # Validate children
        if 'children' in value:
            for child in value['children']:
                if child not in asm:
                    print(f"Child {child} of {key} does not exist in ASM")


def add_folder_path(asm: Dict[str, ActionMetadata]):
    for key, value in asm.items():
        asm[key]['internal'] = True
    return asm


# Example usage
with open('aga_swarm/actions/action_space_metadata.json') as f:
    action_space_metadata = json.load(f)

validate_asm(action_space_metadata)

pp = add_folder_path(action_space_metadata)

# Write the new ASM to a file
with open('aga_swarm/actions/action_space_metadata2.json', 'w') as f:
    json.dump(pp, f, indent=4)