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

from typing import Dict, List, Optional

from pydantic import BaseModel, Field
from typing_extensions import Literal

from swarmstar.utils.misc.generate_uuid import generate_uuid
from swarmstar.utils.misc.generate_uuid import generate_uuid
from swarmstar.utils.data import MongoDBWrapper
from swarmstar.models.internal_metadata import SwarmstarInternal

db = MongoDBWrapper()
ss_internal = SwarmstarInternal()

class MemoryMetadata(BaseModel):
    id: Optional[str] = Field(default_factory=lambda: generate_uuid('memory'))
    type: Literal["internal_folder", "local_folder", "azure_blob"]
    name: str
    description: str
    parent: str
    children: List[str]
    metadata: Dict[str, str]

    @staticmethod
    def get_memory_metadata(memory_id: str) -> 'MemoryMetadata':
        try:
            memory_metadata = db.get("memory_space", memory_id)
            if memory_metadata is None:
                raise ValueError(
                    f"This memory id: `{memory_id}` does not exist in external memory space."
                )
    
        except Exception as e1:
            try:
                memory_metadata = ss_internal.get_internal_memory_metadata(memory_id)
                if memory_metadata is None:
                    raise ValueError(
                        f"This memory id: `{memory_id}` does not exist in internal memory space."
                    ) from e1
            except Exception as e2:
                raise ValueError(
                    f"This memory id: `{memory_id}` does not exist in both internal and external memory spaces."
                ) from e2

        type_mapping = {

        }
        memory_type = memory_metadata["type"]
        if memory_type in type_mapping:
            return type_mapping[memory_type](**memory_metadata)
        return MemoryMetadata(**memory_metadata)
