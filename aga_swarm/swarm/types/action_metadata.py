'''
Every node in the swarm corresponds to an action.

The action space metadata organizes the actions and is used to search
for actions and execute them.

Every action expects the same input: directive, swarm_config and node_id

The actual actions are all prewritten code. The action space metadata's
purpose is:

(1) To allow the swarm to organize and search for actions
(2) To allow the swarm to execute actions

Because the swarm can dynamically create actions we need (2). For example,
we have all the predefined internal actions. So far these are all executed by
importing the main function from the import path. However, when the swarm
dynamically creates actions, they will be stored in the swarm space, on the user's
platform. Actions might be written in different languages, and actions might
have different methods of execution. The action space metadata provides a way
to execute these actions.
'''

from pydantic import BaseModel, Field, RootModel
from typing import Dict, List, Optional, Union, Literal
from enum import Enum

class ActionType(Enum):
    python_main_function = 'python_main_function'

class ActionFolder(BaseModel):
    type: Literal['folder'] = Field('folder', Literal=True)        
    name: str       
    description: str                                             
    children: List[str] = []                                      
    parent: Optional[str] = None                           
    folder_path: str    
    internal: bool
    

class ActionMetadata(BaseModel):
    type: Literal['action'] = Field('action', Literal=True)        
    name: str                   
    description: str     
    parent: str                                                                              
    dependencies: List[str]     # the packages that this action needs installed
    import_path: str
    content_path: str
    language: str 
    internal: bool
    action_type: ActionType
    metadata: Optional[Dict[str, str]] = None       # further metadata to define custom behavior for this action

class ActionSpaceMetadata(RootModel):
    root: Dict[str, Union[ActionMetadata, ActionFolder]]

    def __iter__(self):
        return iter(self.root)

    def __getitem__(self, action_id: str) -> Union[ActionMetadata, ActionFolder]:
        action_metadata = self.root[action_id]
        if action_metadata is None:
            raise ValueError(f"This action id {action_id} does not exist.")
        return action_metadata
