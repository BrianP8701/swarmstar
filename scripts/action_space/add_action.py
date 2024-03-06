import os
from dotenv import load_dotenv
import json

from swarmstar.utils.ai.openai_instructor import completion
from swarmstar.types import InternalAction

load_dotenv() # Load environment variables from .env file

openai_key = os.getenv('OPENAI_KEY')
if not openai_key:
    raise ValueError("OPENAI_KEY not found in .env file.")

def manually_add_internal_action_to_action_space(file_path: str, action_name: str,  description: str, termination_policy: str):
    # Ensure the file_path is relative to 'swarmstar/actions' and format it accordingly
    base_path = 'swarmstar/actions'
    if file_path == base_path:
        raise ValueError(f"The action must be within the '{base_path}' directory.")
    if base_path not in file_path:
        raise ValueError(f"The action must be within the '{base_path}' directory.")
    # Extract the relative path from the full file_path
    relative_path_index = file_path.index(base_path)
    file_path = file_path[relative_path_index:].strip('/').rsplit('.', 1)[0]
    parent_path = '/'.join(file_path.split('/')[:-1]).strip('/')
    # Convert file_path to an import path by replacing '/' with '.'
    import_path = file_path.replace('/', '.')
    
    action_metadata = InternalAction(
        name=action_name,
        description=description,
        parent=parent_path,
        termination_policy=termination_policy,
        internal_action_path=import_path
    )
    
    action_metadata = action_metadata.model_dump()
    with open('swarmstar/actions/action_space.json', 'r+') as file:
        data = json.load(file)
        data[file_path] = action_metadata
        data[parent_path]['children_ids'].append(file_path)
        file.seek(0)
        json.dump(data, file)
        file.truncate()
    
description = (
    "This agent is called when all the children of a 'DecomposeDirective' "
    "node have terminated.\n\nIt is crucial to note, the 'DecomposeDirective' "
    "node breaks a directive into parallel subdirectives to be executed "
    "independently. There may still be further steps that need to be taken "
    "following the completion of this set of subdirectives.\n\nThis agent will "
    "confirm the completion of the directive. If complete, it will terminate "
    "and signal the parent node to terminate as well. Otherwise, it will spawn "
    "a new 'Decompose Directive' node to continue the process."
)
manually_add_internal_action_to_action_space(
    file_path='swarmstar/actions/reasoning/confirm_completion.py', 
    action_name='ConfirmCompletion', 
    description=description,
    termination_policy='simple'
)
