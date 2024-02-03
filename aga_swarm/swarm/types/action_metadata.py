'''
The action space metadata organizes the actions and 
is used by the action router to find the next action to execute.
'''

from pydantic import BaseModel, Field, RootModel
from typing import Dict, List, Optional, Union, Literal
from enum import Enum

class ActionType(Enum):
    main_function = 'main_function'

class ConsumerMetadataType(Enum):
    action = 'action'
    util = 'util'

class ConsumerMetadata(BaseModel):
    type: ConsumerMetadataType
    consumer_id: str

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
    consumers: List[ConsumerMetadata]        # the list of actions or utils that use this action
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
