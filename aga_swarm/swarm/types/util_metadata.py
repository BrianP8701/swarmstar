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

from aga_swarm.utils.data.internal_operations import get_internal_util_metadata
from aga_swarm.utils.data.kv_operations.main import retrieve_swarm_space_kv_value
from aga_swarm.swarm.types.swarm import Swarm

class ConsumerMetadataType(Enum):
    ACTION = 'action'
    UTIL = 'util'

class ConsumerMetadata(BaseModel):
    type: ConsumerMetadataType
    consumer_id: str

class UtilType(Enum):
    INTERNAL_FOLDER = 'internal_folder'
    INTERNAL_FUNCTION = 'internal_function'

class UtilFolder(BaseModel):
    type: UtilType
    name: str
    description: str
    children: List[str] = []
    parent: Optional[str] = None
    folder_metadata: Optional[Dict[str, str]] = None 

class UtilMetadata(BaseModel):
    type: UtilType
    name: str
    description: str
    parent: str
    consumers: List[ConsumerMetadata]
    input_schema: BaseModel
    output_schema: BaseModel
    function_metadata: Optional[Dict[str, str]] = None
    
class UtilSpace(BaseModel):
    swarm: Swarm
    
    def __getitem__(self, util_id: str) -> Union[UtilMetadata, UtilFolder]:
        try:
            internal_util_metadata = get_internal_util_metadata(util_id)
            return internal_util_metadata
        except Exception:
            external_util_metadata = retrieve_swarm_space_kv_value(self.swarm, 'util_space', util_id)
            if external_util_metadata is not None:
                return external_util_metadata
            else:
                raise ValueError(f"This util id: `{util_id}` does not exist.")
