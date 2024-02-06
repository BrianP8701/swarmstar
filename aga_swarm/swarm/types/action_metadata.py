'''
Every node in the swarm corresponds to an action.

The action space metadata organizes the actions and is used to search
for actions and execute them.

Every action has the same IO: 
    directive: str, swarm: Swarm and node_id: str

The actual actions are all prewritten code. The action space metadata's
purpose is:

    (1) To allow the swarm to organize and search for actions
    (2) To allow the swarm to execute actions

Because the swarm can dynamically create actions we need (2). For example,
we might need to dynamically spin up a docker container and execute a function.
The execution_metadata provides a place to store the information to be passed
to the executor who handles this action_type.
'''

from pydantic import BaseModel, RootModel
from typing import Dict, List, Optional, Union
from enum import Enum

from aga_swarm.swarm.types.swarm import Swarm
from aga_swarm.swarm_utils.swarm_space.kv_operations.main import retrieve_swarm_space_kv_value, upload_swarm_space_kv_pair, delete_swarm_space_kv_pair

class ActionType(Enum):
    INTERNAL_FOLDER = 'internal_folder'                             # Folder inside the package
    AZURE_BLOB_STORAGE_FOLDER = 'azure_blob_storage_folder'         # Folder inside azure blob storage
    INTERNAL_PYTHON_MAIN = 'internal_python_main'                   # Python file with main function inside package
    SUBPROCESS_MAIN = 'subprocess_main'                             # Python file with main function outside package stored locally
    AZURE_BLOB_STORAGE_SCRIPT = 'azure_blob_storage_script'         # Python file with main function inside azure blob storage
    AZURE_BLOB_STORAGE_PACKAGE = 'azure_blob_storage_package'       # Package inside azure blob storage

class ActionFolder(BaseModel):
    type: ActionType        
    name: str       
    description: str                                             
    children: List[str] = []                                      
    parent: Optional[str] = None                           
    folder_metadata: Optional[Dict[str, str]] = None
    
class ActionMetadata(BaseModel):
    type: ActionType       
    name: str                   
    description: str     
    parent: str                                                                              
    execution_metadata: Optional[Dict[str, str]] = None       # further metadata to define custom behavior for this action

class ActionSpace(RootModel):
    root: Dict[str, Union[ActionMetadata, ActionFolder]]

    def __iter__(self):
        return iter(self.root)

    def __getitem__(self, action_id: str) -> Union[ActionMetadata, ActionFolder]:
        action_metadata = self.root[action_id]
        if action_metadata is None:
            raise ValueError(f"This action id {action_id} does not exist.")
        return action_metadata
    
    def get_action(swarm: Swarm, action_id: str):
        return retrieve_swarm_space_kv_value(swarm, 'action_space', action_id)
    
    def add_action_space_node(action_id: str, action_metadata: ActionMetadata) -> None:
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
    
    def delete_action_space_node(self, action_id: str) -> None:
        '''
        Delete an action space node and all it's children 
        from the action space and action space metadata.
        
        For now, this operates exclusively on the default
        swarm space. 

        Args:
            action_id (str): The id of the action to delete.
            action_space_metadata (dict): The action space metadata.
        '''
        action_space_metadata = self.get_action_space_metadata()
        action_space_metadata = self._delete_action_space_node_and_all_children(action_id, action_space_metadata)
        self.save_action_space_metadata(action_space_metadata)


    '''
        Private Methods
    '''

    def _delete_action_space_node_and_all_children(self, action_id: str, action_space_metadata: ActionSpace) -> None:
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
                self._delete_action_space_node_and_all_children(child, action_space_metadata)
            self._delete_action_node_helper(action_id, action_space_metadata)
        else:
            self._delete_action_node_helper(action_id, action_space_metadata)

    def _delete_action_node_helper(self, action_id: str, action_space_metadata: ActionSpace):
        '''
        Delete an action from the action space and action space metadata.
        
        Only call this function after all its children have been deleted.
        '''
        action_metadata = action_space_metadata.root[action_id]
        if action_metadata.type == 'action':
            self._delete_file(action_metadata.script_path)
        elif action_metadata.type == 'folder':
            self._delete_folder(action_metadata.folder_path)
        
        parent_id = action_metadata.parent
        parent_metadata = action_space_metadata.root[parent_id]
        parent_metadata.children.remove(action_id)
        del action_space_metadata.root[action_id]




'''
Below is just documentation for what is expected in execution_metadata given an action_type
'''

# For action_type INTERNAL_PYTHON_MAIN_FUNCTION
class InternalPythonMainFunctionMetadata(BaseModel):
    import_path: str
    content_path: str
    
# For action_type SUBPROCESS_MAIN_FUNCTION
class SubprocessMainFunctionMetadata(BaseModel):
    import_path: str
    content_path: str
    
# Idk abt the other ones yet
# TODO add the other ones