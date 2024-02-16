'''
The memory metadata is a place for the swarm to store it's work,
as well as a place for it to perform various forms of RAG. 

First and foremost, the memory metadata organizes the memory so 
routers can search over the space effectively.

Secondly, data can take on many forms. Internal package documentation,
cloud blob storage, local file systems, vector databases and more.
All of these require different types of interaction. The memory 
metadata labels the memory so the swarm knows how to interact with it.
'''
from enum import Enum
from typing import List, Optional, Dict, Union
from pydantic import BaseModel

from tree_swarm.utils.data.internal_operations import get_internal_memory_metadata
from tree_swarm.utils.data.kv_operations.main import get_kv
from tree_swarm.swarm.types import Swarm
    
class MemoryType(Enum):
    INTERNAL_FOLDER = "internal_folder"
    INTERNAL_PYTHON_FILE = "internal_python_file"
    INTERNAL_MARKDOWN_FILE = "internal_markdown_file"
    LOCAL_FOLDER = "local_folder"
    LOCAL_PYTHON_FILE = "local_python_file"
    LOCAL_MARKDOWN_FILE = "local_markdown_file"
    LOCAL_JSON = "local_json"
    AZURE_COSMOS_DB_CONTAINER = "azure_cosmos_db_container"
    AZURE_BLOB = "azure_blob"
    
class MemoryFolder(BaseModel):
    type: MemoryType
    name: str
    description: str
    children: List[str]
    parent: Optional[str] = None
    folder_metadata: Optional[Dict[str, str]] = None

class MemoryMetadata(BaseModel):
    type: MemoryType
    name: str
    description: str
    parent: str
    metadata: Optional[Dict[str, str]] = None      # further metadata to define custom behavior for this memory
    
class MemorySpace(BaseModel):
    swarm: Swarm

    def __getitem__(self, memory_id: str) -> Union[MemoryMetadata, MemoryFolder]:
        try:
            internal_memory_metadata = get_internal_memory_metadata(memory_id)
            return internal_memory_metadata
        except Exception:
            external_memory_metadata = get_kv(self.swarm, 'memory_space', memory_id)
            if external_memory_metadata is not None:
                return external_memory_metadata
            else:
                raise ValueError(f"This memory id: `{memory_id}` does not exist.")
    
'''
Below is just documentation for what is expected in execution_metadata given a memory_type
'''

class LocalPythonFileMetadata(BaseModel):
    import_path: str
    
class LocalJsonMetadata(BaseModel):
    import_path: str
    
class AzureCosmosDbContainerMetadata(BaseModel):
    database_name: str
    container_name: str
    partition_key: str
    # TODO more make this work ik this isnt accurate yet
    
class AzureBlobMetadata(BaseModel):
    container_name: str
    blob_name: str
    # TODO more make this work ik this isnt accurate yet
