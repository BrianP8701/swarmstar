from enum import Enum
from pydantic import BaseModel, RootModel, Field
from typing import Dict, List, Literal, Optional, Union


'''
    Action Space Metadata
'''

class Property(BaseModel):
    type: str
    description: str
    enum: Optional[List[str]] = None

class ActionMetadata(BaseModel):
    type: Literal['action'] = Field('action', Literal=True)
    name: str
    description: str
    input_schema: Dict[str, Property] = {}
    output_schema: Dict[str, Property] = {}
    dependencies: List[str] = []
    parent: str = None
    script_path: str = None
    language: str
    internal: bool
    
class ActionFolderMetadata(BaseModel):
    type: Literal['folder'] = Field('folder', Literal=True)
    name: str
    description: str
    children: List[str]
    parent: Optional[str] = None
    folder_path: str
    internal: bool

class ActionSpaceMetadata(RootModel):
    root: Dict[str, Union[ActionMetadata, ActionFolderMetadata]]

'''
    Memory Space Metadata
'''

class MemoryType(Enum):
    INTERNAL_SWARM_FOLDER = "internal_swarm_folder"
    MEMORY = "memory"
    INTERNAL_SWARM_MEMORY = "internal_swarm_memory"
    
class MemoryMetadata(BaseModel):
    type: MemoryType
    name: str
    description: str
    children:Optional[List[str]] = []
    
class MemorySpaceMetadata(Dict[str, MemoryMetadata]):
    pass