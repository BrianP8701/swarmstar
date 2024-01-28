from aga_swarm.swarm.types import *
from pydantic import ValidationError
import json

action_space_path = 'aga_swarm/actions/action_space_metadata.json'
memory_space_path = 'aga_swarm/memory/memory_space_metadata.json'

def validate_action_space(file_path: str) -> bool:
    try:
        with open(file_path, 'r') as f:
            data = json.load(f)
        ActionSpaceMetadata(**data)
        print("The JSON file follows the ActionSpaceMetadata schema.")
        return True
    except (json.JSONDecodeError, ValidationError) as e:
        print(f"The JSON file does not follow the ActionSpaceMetadata schema. Error: {e}")
        return False
    
def validate_memory_space(file_path: str) -> bool:
    try:
        with open(file_path, 'r') as f:
            data = json.load(f)
        MemorySpaceMetadata(**data)
        print("The JSON file follows the MemorySpaceMetadata schema.")
        return True
    except (json.JSONDecodeError, ValidationError) as e:
        print(f"The JSON file does not follow the MemorySpaceMetadata schema. Error: {e}")
        return False
    
validate_action_space(action_space_path)

