'''
Every node in the swarm corresponds to an action.

The action space metadata organizes the actions and is used to search
for actions and execute them.

Every action has the same IO: 
    message: str, swarm: Swarm and node_id: str

The actual actions are all prewritten code. The action space metadata's
purpose is:

    (1) To allow the swarm to organize and search for actions
    (2) To allow the swarm to execute actions

Because the swarm can dynamically create actions we need (2). For example,
we might need to dynamically spin up a docker container and execute a function.
The execution_metadata provides a place to store the information to be passed
to the executor who handles this action_type.
'''
from __future__ import annotations
from pydantic import BaseModel
from typing import Dict, List, Optional, Union
from enum import Enum
from typing import TYPE_CHECKING

from aga_swarm.utils.data.kv_operations.main import retrieve_swarm_space_kv_value
from aga_swarm.utils.data.internal_operations import get_internal_action_metadata

if TYPE_CHECKING:
    from aga_swarm.swarm.types.swarm import Swarm
    
class ActionType(Enum):
    INTERNAL_FOLDER = 'internal_folder'                             # Folder inside the package
    AZURE_BLOB_STORAGE_FOLDER = 'azure_blob_storage_folder'         # Folder inside azure blob storage
    INTERNAL_PYTHON_MAIN = 'internal_python_main'                   # Python file with main function inside package
    INTERNAL_PYTHON_FUNCTION = 'internal_python_function'           # Python file with function name in execution_metadata
    SUBPROCESS_MAIN = 'subprocess_main'                             # Python file with main function outside package stored locally
    AZURE_BLOB_STORAGE_SCRIPT = 'azure_blob_storage_script'         # Python file with main function inside azure blob storage
    AZURE_BLOB_STORAGE_PACKAGE = 'azure_blob_storage_package'       # Package inside azure blob storage

class ActionMetadata(BaseModel):
    is_folder: bool
    type: ActionType        
    name: str       
    description: str                                             
    children: Optional[List[str]] = None                                      
    parent: Optional[str] = None                           
    folder_metadata: Optional[Dict[str, str]] = None
    execution_metadata: Optional[Dict[str, str]] = None

class ActionSpace(BaseModel):
    '''
    The action space metadata is stored in the swarm's kv store as:
    
        action_id: ActionMetadata
    '''
    swarm: Swarm
    
    def __getitem__(self, action_id: str) -> ActionMetadata:
        try:
            internal_action_metadata = get_internal_action_metadata(action_id)
            return internal_action_metadata
        except Exception:
            external_action_metadata = retrieve_swarm_space_kv_value(self.swarm, 'action_space', action_id)
            if external_action_metadata is not None:
                return external_action_metadata
            else:
                raise ValueError(f"This action id: `{action_id}` does not exist.")
            
    def get_root(self) -> ActionMetadata:
        return self['aga_swarm/actions']
    




'''
Below is just documentation for what is expected in execution_metadata given an action_type
'''

# For action_type INTERNAL_PYTHON_MAIN_FUNCTION
class InternalPythonMainFunctionMetadata(BaseModel):
    script_path: str

class InternalPythonFunctionMetadata(BaseModel):
    script_path: str
    function_name: str
    
# For action_type SUBPROCESS_MAIN_FUNCTION
class SubprocessMainFunctionMetadata(BaseModel):
    import_path: str
    content_path: str
    
# Idk abt the other ones yet
# TODO add the other ones