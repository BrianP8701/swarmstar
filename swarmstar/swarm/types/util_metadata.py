"""
The swarm util space metadata has a simlar but different role to 
the action space metadata:

    (1) To allow the swarm to organize and search for utils
    (2) Describe how to interact with the utils

Swarm utils are just swarm specific functions. They may be
used in the construction of actions.

For now we assume all utils are internal to the package.
"""
from typing import Dict, List, Optional

from pydantic import BaseModel, Field
from typing_extensions import Literal

from swarmstar.utils.misc.uuid import generate_uuid

class UtilMetadata(BaseModel):
    id: Optional[str] = Field(default_factory=lambda: generate_uuid('util'))
    type: Literal["internal_folder", "internal_function"]
    name: str
    description: str
    parent: str
    children: List[str] = []
    metadata: Dict[str, str]
