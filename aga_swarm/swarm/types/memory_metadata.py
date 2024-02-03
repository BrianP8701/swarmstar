from enum import Enum
from typing import List, Optional, Dict, Literal
from pydantic import BaseModel, Field

class MemoryType(Enum):
    FOLDER = "folder"
    KVSTORE = "kv_store"
    FILESTORE = "file_store"
    UTIL = "util"
    ACTION = "action"
    
class MemoryFolder(BaseModel):
    type: Literal['folder'] = Field('folder', Literal=True)
    name: str
    description: str
    children:Optional[List[str]] = []
    internal: bool

class ActionMemory(BaseModel):
    type: Literal['action'] = Field('action', Literal=True)
    internal: bool
    content_path: str
    import_path: str
    dependencies: List[str]
    language: str
    consumers: List[str]

class MemoryMetadata(BaseModel):
    type: Literal['memory'] = Field('memory', Literal=True)
    memory_type: MemoryType
    name: str
    description: str
    children:Optional[List[str]] = []
    internal: bool
    content_path: str
    import_path: str
    
class MemorySpaceMetadata(Dict[str, MemoryMetadata]):
    pass