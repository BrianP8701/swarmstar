from pydantic import BaseModel
from enum import Enum
from typing import Dict, List, Optional


'''
    Action Space Metadata
'''

class ActionType(Enum):
    INTERNAL_SWARM_FOLDER = "internal_swarm_folder"
    ACTION = "action"
    INTERNAL_DEFAULT_SWARM_ACTION = "internal_default_swarm_action"
    DEFAULT_SWARM_ACTION = "default_swarm_action"

class Property(BaseModel):
    type: str
    description: str
    enum: Optional[List[str]] = None

class ActionMetadata(BaseModel):
    type: ActionType
    name: str
    description: str
    input_schema: Optional[Dict[str, Property]] = {}
    output_schema: Optional[Dict[str, Property]] = {}
    dependencies: Optional[List[str]] = []
    children: Optional[List[str]] = []

class ActionSpaceMetadata(Dict[str, ActionMetadata]):
    pass


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