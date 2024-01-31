from enum import Enum
from typing import List, Optional, Dict
from pydantic import BaseModel

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