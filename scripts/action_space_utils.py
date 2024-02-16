from typing import Union
import json
import sqlite3

from tree_swarm.swarm.types import ActionMetadata, ActionFolder, ActionType

def change_action_space_metadata(key: str, metadata: Union[ActionFolder, ActionMetadata]):
    json_path = 'tree_swarm/actions/action_space_metadata.json'
    sqlite3_path = 'tree_swarm/actions/action_space_metadata.sqlite3'
    
    # Change the key value pair in both files
    with open(json_path, 'r') as f:
        action_space_metadata = json.load(f)
    action_space_metadata[key] = metadata
    with open(json_path, 'w') as f:
        json.dump(action_space_metadata, f)

    conn = sqlite3.connect(sqlite3_path)
    c = conn.cursor()
    c.execute("UPDATE kv_store SET key = ? WHERE key = 1", (metadata,))
    conn.commit()
    conn.close()



    



action_id = "tree_swarm/actions/reasoning/decompose_directive"


dict_version = {
    "type": "internal_python_main",
    "name": "decompose_directive.py",
    "description": "Decompose directives into immediate parralel sub-directives.",
    "parent": "tree_swarm/actions/reasoning",
    "execution_metadata": {
        "script_path": "tree_swarm/actions/reasoning/decompose_directive.py"
    }
}

metadata = ActionMetadata.model_validate(dict_version)




change_action_space_metadata('tree_swarm/actions/reasoning/decompose_directive', dict_version)



# def add_action_space_node(action_id: str, action_metadata: ActionMetadata) -> None:
#     '''
#     Simply adds an action space node to the action space and 
#     action space metadata.
    
#     Args:
#         action_id (str): The id of the action to add. This is the key in the action space metadata.
#         action_space_metadata (dict): The action space metadata.
#         action_metadata (ActionMetadata): The action metadata.
#     '''
#     action_space_metadata.root[action_id] = action_metadata
#     parent_id = action_metadata.parent
#     parent_metadata = action_space_metadata.root[parent_id]
#     parent_metadata.children.append(action_id)

# def delete_action_space_node(self, action_id: str) -> None:
#     '''
#     Delete an action space node and all it's children 
#     from the action space and action space metadata.
    
#     For now, this operates exclusively on the default
#     swarm space. 

#     Args:
#         action_id (str): The id of the action to delete.
#         action_space_metadata (dict): The action space metadata.
#     '''
#     action_space_metadata = self.get_action_space_metadata()
#     action_space_metadata = self._delete_action_space_node_and_all_children(action_id, action_space_metadata)
#     self.save_action_space_metadata(action_space_metadata)


# '''
#     Private Methods
# '''

# def _delete_action_space_node_and_all_children(self, action_id: str, action_space_metadata: ActionSpace) -> None:
#     '''
#     Helper function for delete_action_space_node. Recursively
#     deletes all children of the action space node and then the
#     node itself. Returns the updated action space metadata.
#     '''
#     action_metadata = action_space_metadata.root[action_id]
#     if action_metadata is None:
#         raise ValueError(f"This action id {action_id} does not exist.")
        
#     if action_metadata.type == 'folder':
#         for child in list(action_metadata.children):
#             self._delete_action_space_node_and_all_children(child, action_space_metadata)
#         self._delete_action_node_helper(action_id, action_space_metadata)
#     else:
#         self._delete_action_node_helper(action_id, action_space_metadata)

# def _delete_action_node_helper(self, action_id: str, action_space_metadata: ActionSpace):
#     '''
#     Delete an action from the action space and action space metadata.
    
#     Only call this function after all its children have been deleted.
#     '''
#     action_metadata = action_space_metadata.root[action_id]
#     if action_metadata.type == 'action':
#         self._delete_file(action_metadata.script_path)
#     elif action_metadata.type == 'folder':
#         self._delete_folder(action_metadata.folder_path)
    
#     parent_id = action_metadata.parent
#     parent_metadata = action_space_metadata.root[parent_id]
#     parent_metadata.children.remove(action_id)
#     del action_space_metadata.root[action_id]