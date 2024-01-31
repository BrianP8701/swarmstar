import os
import shutil
from pydantic import validate_call
from aga_swarm.swarm.types import *

@validate_call
def delete_action_space_node(action_id: str, action_space_metadata: ActionSpaceMetadata):
    '''
    Delete an action space node and all it's children 
    from the action space and action space metadata.
    
    For now, this operates exclusively on the default
    swarm space. 

    Args:
        action_id (str): The id of the action to delete.
        action_space_metadata (dict): The action space metadata.
    '''
    action_metadata = action_space_metadata['action_id']
    if action_metadata is None:
        raise ValueError(f"This action id {action_id} does not exist.")
    
    if action_metadata['type'] == 'folder':
        for child in action_metadata.children:
            delete_action_space_node(child, action_space_metadata)
        _delete_action(action_id, action_space_metadata)
    else:
        _delete_action(action_id, action_space_metadata)
    
@validate_call
def add_action_space_node(action_id: str, action_space_metadata: ActionSpaceMetadata, action_metadata: ActionMetadata):
    '''
    Simply adds an action space node to the action space and 
    action space metadata.
    
    Args:
        action_id (str): The id of the action to add. This is the key in the action space metadata.
        action_space_metadata (dict): The action space metadata.
        action_metadata (ActionMetadata): The action metadata.
    '''
    action_space_metadata[action_id] = action_metadata
    parent_id = action_metadata.parent
    parent_metadata = action_space_metadata[parent_id]
    parent_metadata.children.append(action_id)
    
def _delete_action(action_id: str, action_space_metadata: ActionSpaceMetadata):
    '''
    Delete an action from the action space and action space metadata.
    
    Only call this function after all its children have been deleted.
    '''
    action_metadata = action_space_metadata[action_id]
    if action_metadata.type == 'action':
        os.remove(action_metadata.script_path)
    elif action_metadata.type == 'folder':
        shutil.rmtree(action_metadata.folder_path)
    
    parent_id = action_metadata.parent
    parent_metadata = action_space_metadata[parent_id]
    parent_metadata.children.remove(action_id)
    
    del action_space_metadata[action_id]
