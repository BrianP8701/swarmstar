import os
import shutil
from pydantic import validate_call
from typing import Dict, Union

from aga_swarm.utils.swarm_utils import get_action_space_metadata, save_action_space_metadata
from aga_swarm.swarm.types import *

@validate_call
def delete_action_space_node(action_id: str, swarm_id: SwarmID) -> None:
    '''
    Delete an action space node and all it's children 
    from the action space and action space metadata.
    
    For now, this operates exclusively on the default
    swarm space. 

    Args:
        action_id (str): The id of the action to delete.
        action_space_metadata (dict): The action space metadata.
    '''
    action_space_metadata = get_action_space_metadata(swarm_id)
    action_space_metadata = _delete_action_space_node_recursive_helper(action_id, action_space_metadata)
    save_action_space_metadata(swarm_id, action_space_metadata)

@validate_call
def add_action_space_node(action_id: str, action_space_metadata: ActionSpaceMetadata, action_metadata: ActionMetadata) -> None:
    '''
    Simply adds an action space node to the action space and 
    action space metadata.
    
    Args:
        action_id (str): The id of the action to add. This is the key in the action space metadata.
        action_space_metadata (dict): The action space metadata.
        action_metadata (ActionMetadata): The action metadata.
    '''
    action_space_metadata.root[action_id] = action_metadata
    parent_id = action_metadata.parent
    parent_metadata = action_space_metadata.root[parent_id]
    parent_metadata.children.append(action_id)


'''
    Private Methods
'''

def _delete_action_space_node_recursive_helper(action_id: str, action_space_metadata: ActionSpaceMetadata) -> None:
    '''
    Helper function for delete_action_space_node. Recursively
    deletes all children of the action space node and then the
    node itself. Returns the updated action space metadata.
    '''
    action_metadata = action_space_metadata.root[action_id]
    if action_metadata is None:
        raise ValueError(f"This action id {action_id} does not exist.")
        
    if action_metadata.type == 'folder':
        for child in list(action_metadata.children):
            _delete_action_space_node_recursive_helper(child, action_space_metadata)
        _delete_action(action_id, action_space_metadata)
    else:
        _delete_action(action_id, action_space_metadata)
        
    return action_space_metadata

def _delete_action(action_id: str, action_space_metadata: ActionSpaceMetadata):
    '''
    Delete an action from the action space and action space metadata.
    
    Only call this function after all its children have been deleted.
    '''
    action_metadata = action_space_metadata.root[action_id]
    if action_metadata.type == 'action':
        os.remove(action_metadata.script_path)
    elif action_metadata.type == 'folder':
        shutil.rmtree(action_metadata.folder_path)
    
    parent_id = action_metadata.parent
    parent_metadata = action_space_metadata.root[parent_id]
    parent_metadata.children.remove(action_id)
    
    del action_space_metadata.root[action_id]
