'''
The swarm util space metadata has a simlar but different role to 
the action space metadata:

(1) To allow the swarm to organize and search for utils
(2) Describe how to interact with the utils

Swarm utils are just swarm specific functions. They may be
used in the construction of actions.
'''

from pydantic import BaseModel, Field, RootModel
from typing import Dict, List, Optional, Union, Literal
from enum import Enum

class ConsumerMetadataType(Enum):
    ACTION = 'action'
    UTIL = 'util'

class ConsumerMetadata(BaseModel):
    type: ConsumerMetadataType
    consumer_id: str

class SwarmUtilFolder(BaseModel):
    type: Literal['folder'] = Field('folder', Literal=True)
    name: str
    description: str
    children: List[str] = []
    parent: Optional[str] = None
    folder_path: str    
    internal: bool

class SwarmFunctionMetadata(BaseModel):
    type: Literal['function'] = Field('function', Literal=True) 
    name: str
    description: str
    parent: str
    dependencies: List[str]  
    consumers: List[ConsumerMetadata]
    import_path: str
    function_name: str
    language: str
    internal: bool
    input_schema: BaseModel
    output_schema: BaseModel
    metadata: Optional[Dict[str, str]] = None
    
class SwarmUtilSpaceMetadata(RootModel):
    root: Dict[str, Union[SwarmFunctionMetadata, SwarmUtilFolder]]

    def __iter__(self):
        return iter(self.root)
    
    def __getitem__(self, util_id: str) -> Union[SwarmFunctionMetadata, SwarmUtilFolder]:
        util_metadata = self.root[util_id]
        if util_metadata is None:
            raise ValueError(f"This util id {util_id} does not exist.")
        return util_metadata