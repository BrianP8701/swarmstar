from enum import Enum
from pydantic import BaseModel, RootModel, Field
from typing import Dict, List, Literal, Optional, Union


'''
    Action Space Metadata
'''

class Property(BaseModel):
    type: str                                                       # the type of the property
    description: str                                                # the description of the property
    enum: Optional[List[str]] = None                                # optional list of possible values of the property

class ActionMetadata(BaseModel):
    type: Literal['action'] = Field('action', Literal=True)         # this is always 'action'
    name: str                                                       # the human readable name of the action
    description: str                                                # concise & comprehensive description of the action
    input_schema: Dict[str, Property] = {}                          # the input schema of the action
    output_schema: Dict[str, Property] = {}                         # the output schema of the action
    dependencies: List[str] = []                                    # the list of packages that this action depends on
    parent: str = None                                              # the parent folder of the action
    script_path: str = None                                         # the path to the script that the action runs
    language: str = None                                            # the language that the action is written in
    internal: bool = False                                          # whether the action is inside the package or custom
    content_path: str = None                                        # the path to the content of the action
    
class ActionFolderMetadata(BaseModel):
    type: Literal['folder'] = Field('folder', Literal=True)         # this is always 'folder'
    name: str                                                       # the human readable name of the folder
    description: str                                                # the description of the folder
    children: List[str] = []                                        # the list of children of the folder
    parent: Optional[str] = None                                    # the parent folder of the folder
    folder_path: str = None                                         # the path to the folder
    internal: bool = False                                          # whether the folder is inside the package or custom

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