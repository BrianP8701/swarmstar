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

from typing import Dict, List

from pydantic import BaseModel
from typing_extensions import Literal

from swarmstar.swarm.types.swarm_config import SwarmConfig
from swarmstar.utils.data.internal_operations import get_internal_memory_metadata
from swarmstar.utils.data.kv_operations.main import get_kv


class MemoryMetadata(BaseModel):
    type: Literal["internal_folder", "local_folder", "azure_blob"]
    name: str
    description: str
    parent: str
    children: List[str]
    metadata: Dict[str, str]


class MemorySpace(BaseModel):
    swarm: SwarmConfig

    def __getitem__(self, memory_id: str) -> MemoryMetadata:
        try:
            internal_memory_metadata = get_internal_memory_metadata(
                self.swarm, memory_id
            )
            return internal_memory_metadata
        except Exception:
            external_memory_metadata = get_kv(self.swarm, "memory_space", memory_id)
            if external_memory_metadata is not None:
                return external_memory_metadata
            else:
                raise ValueError(f"This memory id: `{memory_id}` does not exist.")
