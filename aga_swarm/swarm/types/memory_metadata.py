'''
The memory metadata is a place for the swarm to store it's work,
as well as a place for it to perform various forms of RAG. 

First and foremost, the memory metadata organizes the memory so 
routers can search over the space effectively.

Secondly, data can take on many forms. Internal package documentation,
cloud blob storage, local file systems, vector databases and more.
All of these require very different types of interaction. The memory 
metadata labels the memory so the swarm knows how to interact with it.
'''

from enum import Enum
from typing import List, Optional, Dict, Union, Any
from pydantic import BaseModel, RootModel

class MemoryType(Enum):
    INTERNAL_FOLDER = "internal_folder"
    INTERNAL_JSON = "internal_json"
    INTERNAL_PYTHON_PACKAGE = "internal_python_package"
    INTERNAL_PYTHON_FILE = "internal_python_file"
    LOCAL_FOLDER = "local_folder"
    LOCAL_JSON = "local_json"
    LOCAL_FILE = "local_file"
    AZURE_COSMOS_DB = "azure_cosmos_db"
    GOOGLE_FIRESTORE = "google_firestore"
    AZURE_BLOB_STORAGE = "azure_blob_storage"
    
class MemoryFolder(BaseModel):
    type: MemoryType
    name: str
    description: str
    parent: Optional[str] = None
    children: List[str]
    folder_path: str
    internal: bool

class MemoryMetadata(BaseModel):
    type: MemoryType
    name: str
    description: str
    internal: bool
    content_path: str
    parent: str
    metadata: Optional[Dict[str, str]] = None      # further metadata to define custom behavior for this memory
    
class MemorySpaceMetadata(RootModel):
    root: Dict[str, Union[MemoryMetadata, MemoryFolder]]

    def __iter__(self):
        return iter(self.root)
    
    def __getitem__(self, memory_id: str) -> Union[MemoryMetadata, MemoryFolder]:
        memory_metadata = self.root[memory_id]
        if memory_metadata is None:
            raise ValueError(f"This memory id {memory_id} does not exist.")
        return memory_metadata