"""
The memory metadata is a place for the swarm to store it's work,
as well as a place for it to perform various forms of RAG. 

First and foremost, the memory metadata organizes the memory so 
routers can search over the space effectively.

Secondly, data can take on many forms. Internal package documentation,
cloud blob storage, local file systems, vector databases and more.
All of these require different types of interaction. The memory 
metadata labels the memory so the swarm knows how to interact with it.
"""

from typing import Dict, List, Optional, Any

from pydantic import BaseModel, Field
from typing_extensions import Literal

from swarmstar.utils.misc.generate_uuid import generate_uuid
from swarmstar.utils.misc.generate_uuid import generate_uuid
from swarmstar.utils.data import MongoDBWrapper
from swarmstar.models.internal_metadata import SwarmstarInternal

db = MongoDBWrapper()

class MemoryMetadata(BaseModel):
    id: Optional[str] = Field(default_factory=lambda: generate_uuid('memory'))
    is_folder: bool
    type: Literal[
        "internal_folder",
        "internal_string",
        "folder",
        "project_root_folder",
        "project_file_bytes",
        "string"
    ]
    name: str
    description: str
    parent: Optional[str] = None
    children_ids: Optional[List[str]] = None
    context: Optional[Dict[str, Any]] = {}

    @staticmethod
    def get(memory_id: str) -> 'MemoryMetadata':
        try:
            memory_metadata = db.get("memory_metadata", memory_id)
            if memory_metadata is None:
                raise ValueError(
                    f"This memory id: `{memory_id}` does not exist in external memory space."
                )
    
        except:
            try:
                memory_metadata = SwarmstarInternal.get_memory_metadata(memory_id)
                if memory_metadata is None:
                    raise ValueError(
                        f"This memory id: `{memory_id}` does not exist in internal memory space."
                    )
            except:
                raise ValueError(
                    f"This memory id: `{memory_id}` does not exist in both internal and external memory spaces."
                )

        type_mapping = {

        }
        memory_type = memory_metadata["type"]
        if memory_type in type_mapping:
            return type_mapping[memory_type](**memory_metadata)
        return MemoryMetadata(**memory_metadata)

    @staticmethod
    def clone(swarm_id: str) -> List[str]:
        """
        Copies the internal memory metadata tree with root id as swarm id
        and UUIDs for all the children.
        
        Returns a list of all the memory metadata ids.
        """
        internal_memory_metadata_root = SwarmstarInternal.get_memory_metadata("root")
        internal_memory_metadata_root.id = swarm_id
        MemoryMetadata.save(internal_memory_metadata_root)
        memory_space = [internal_memory_metadata_root]
        
        def recursive_helper(memory_metadata: 'MemoryMetadata'):
            if memory_metadata.children_ids is not None:
                for child_id in memory_metadata.children_ids:
                    child_metadata = SwarmstarInternal.get_memory_metadata(child_id)
                    child_metadata.id = f"{swarm_id}_{child_metadata.id}"
                    memory_space.append(child_metadata)
                    MemoryMetadata.save(child_metadata)
                    recursive_helper(child_metadata)

        recursive_helper(internal_memory_metadata_root)
        return memory_space

    @staticmethod
    def save(memory_metadata: 'MemoryMetadata') -> None:
        db.insert("memory_metadata", memory_metadata.id, memory_metadata.model_dump())

    @staticmethod
    def delete(memory_id: str) -> None:
        db.delete("memory_metadata", memory_id)

    @staticmethod
    def delete_external_memory_metadata_tree(swarm_id: str) -> None:
        root_memory_metadata = MemoryMetadata.get(swarm_id)
        
        def recursive_helper(memory_metadata: 'MemoryMetadata'):
            MemoryMetadata.delete(memory_metadata.id)
            if memory_metadata.children_ids is not None:
                for child_id in memory_metadata.children_ids:
                    child_metadata = MemoryMetadata.get(child_id)
                    recursive_helper(child_metadata)

        recursive_helper(root_memory_metadata)

class MemoryFolder(MemoryMetadata):
    is_folder: Literal[True] = Field(default=True)
    type: Literal[
        "folder",
        "internal_folder",
        "project_root_folder",
    ]
    name: str
    description: str
    children_ids: List[str]
    parent: Optional[str] = None

class MemoryNode(MemoryMetadata):
    is_folder: Literal[False] = Field(default=False)
    type: Literal[
        "project_file_bytes"
    ]
    name: str
    description: str
    parent: str
    children_ids: Optional[List[str]] = Field(default=None)
    context: Optional[Dict[str, Any]] = {}
