"""
The swarm util space metadata has a simlar but different role to 
the action space metadata:

    (1) To allow the swarm to organize and search for utils
    (2) Describe how to interact with the utils

Swarm utils are just swarm specific functions. They may be
used in the construction of actions.

For now we assume all utils are internal to the package.
"""
from typing import Dict, List

from pydantic import BaseModel
from typing_extensions import Literal

class UtilMetadata(BaseModel):
    id: str
    type: Literal["internal_folder", "internal_function"]
    name: str
    description: str
    parent: str
    children: List[str] = []
    metadata: Dict[str, str]
