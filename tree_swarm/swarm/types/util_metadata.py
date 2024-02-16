'''
The swarm util space metadata has a simlar but different role to 
the action space metadata:

    (1) To allow the swarm to organize and search for utils
    (2) Describe how to interact with the utils

Swarm utils are just swarm specific functions. They may be
used in the construction of actions.

For now we assume all utils are internal to the package.
'''
from pydantic import BaseModel
from typing import Dict, List, Optional, Union
from enum import Enum
from typing_extensions import Literal

from tree_swarm.utils.data.internal_operations import get_internal_util_metadata
from tree_swarm.utils.data.kv_operations.main import get_kv
from tree_swarm.swarm.types.swarm import Swarm

class ConsumerMetadataType(Enum):
    ACTION = 'action'
    UTIL = 'util'

class ConsumerMetadata(BaseModel):
    type: ConsumerMetadataType
    consumer_id: str

class UtilType(Enum):
    INTERNAL_FOLDER = 'internal_folder'
    INTERNAL_FUNCTION = 'internal_function'

class UtilMetadata(BaseModel):
    type: Literal['internal_folder', 'internal_function']
    name: str
    description: str
    parent: Optional[str] = None
    children: List[str] = []
    metadata: Optional[Dict[str, str]] = None 
    
class UtilSpace(BaseModel):
    swarm: Swarm
    
    def __getitem__(self, util_id: str) -> UtilMetadata:
        try:
            internal_util_metadata = get_internal_util_metadata(self.swarm, util_id)
            return internal_util_metadata
        except Exception:
            external_util_metadata = get_kv(self.swarm, 'util_space', util_id)
            if external_util_metadata is not None:
                return external_util_metadata
            else:
                raise ValueError(f"This util id: `{util_id}` does not exist.")
