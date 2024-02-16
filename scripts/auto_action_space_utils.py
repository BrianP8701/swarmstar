from pydantic import BaseModel, Field
import os
from dotenv import load_dotenv
import sqlite3
import json

from tree_swarm.utils.ai.openai_instructor import completion
from tree_swarm.swarm.types import ActionMetadata, ActionType

load_dotenv()  # Load environment variables from .env file
openai_key = os.getenv('OPENAI_KEY')
if not openai_key:
    raise ValueError("OPENAI_KEY not found in .env file.")

def save_script_action_to_internal_action_space(script_path: str):
    # Ensure the script_path is relative to 'tree_swarm/actions' and format it accordingly
    if 'tree_swarm/actions' not in script_path:
        raise ValueError("The script path must be within the 'tree_swarm/actions' directory.")
    
    # Make script_path relative to 'tree_swarm/actions'
    relative_script_path = script_path.split('tree_swarm/actions/', 1)[1]
    
    # Ensure the script_path does not start or end with '/'
    relative_script_path = relative_script_path.strip('/')
    
    # Read the script content
    with open(f'tree_swarm/actions/{relative_script_path}', 'r') as file:
        script = file.read()
    
    # Get the parent folder of the script, ensuring it does not start or end with '/'
    parent_path_parts = relative_script_path.split('/')[:-1]
    if not parent_path_parts:
        raise ValueError("The script path must be deeper than the 'tree_swarm/actions' root directory.")
    
    parent_id = 'tree_swarm/actions/' + '/'.join(parent_path_parts)
    
    class DescribeAction(BaseModel):
        description: str = Field(..., description="A clear, comprehensive and concise description of what this action script does. It gets called from the main function always. What does it do? Specific details matter")
    
    system_instructions = ('Generate a clear, comprehensive and concise description of what this action script does. It gets called from the main function always. What does it do? Specific details matter')
    messages = [
        {
            "role": "system",
            "content": system_instructions
        },
        {
            "role": "user",
            "content": f'Directive: \n`{script}`'
        }
    ]

    response = completion(messages=messages, openai_key=openai_key, instructor_model=DescribeAction)
    
    description = response.description
    action_metadata = ActionMetadata(
        is_folder=False,
        type=ActionType.INTERNAL_PYTHON_MAIN,
        name=os.path.splitext(os.path.basename(relative_script_path))[0],
        description=description,
        parent=parent_id,
        execution_metadata={
            "script_path": relative_script_path.replace('/', '.').rsplit('.', 1)[0]
        }
    )
    # conn = sqlite3.connect('tree_swarm/actions/action_space_metadata.sqlite3')
    # cursor = conn.cursor()
    # cursor.execute('INSERT INTO kv_store (key, value) VALUES (?, ?)', (script_path, action_metadata.model_dump_json()))
    
    action_metadata = action_metadata.model_dump()
    action_metadata['type'] = action_metadata['type']
    
    with open('tree_swarm/actions/action_space_metadata.json', 'r+') as file:
        data = json.load(file)
        data[script_path] = action_metadata
        data[parent_id]['children'].append(script_path)
        file.seek(0)
        json.dump(data, file)
        file.truncate()


test1 = 'tree_swarm/actions/reasoning/route_goal.py'

save_script_action_to_internal_action_space(test1)
