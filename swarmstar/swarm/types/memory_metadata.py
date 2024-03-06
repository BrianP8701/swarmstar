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

class MemoryMetadata(BaseModel):
    id: Optional[str] = Field(default_factory=lambda: generate_uuid('memory'))
    type: Literal["internal_folder", "local_folder", "azure_blob"]
    name: str
    description: str
    parent: str
    children: List[str]
    metadata: Dict[str, str]
