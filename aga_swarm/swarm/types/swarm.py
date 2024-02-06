'''
The swarm config is a record of the configuration of the swarm. It
stores all the information about the environment in which the swarm 
is running. It also provides methods to interact with the swarm space.

The swarm config is a small data structure consisting only of strings,
and is passed around between every action. I made this so the swarm
could be decoupled and stateless. This is important for scalability.
'''

from enum import Enum
from pydantic import BaseModel
from typing import Union

from aga_swarm.swarm.types.memory_metadata import MemorySpaceMetadata, MemoryMetadata, MemoryFolder
from aga_swarm.swarm.types.swarm_state import SwarmState
from aga_swarm.swarm.types.swarm_history import SwarmHistory, SwarmEvent
from aga_swarm.swarm_utils.internal_package.get_resources import import_internal_python_action

class Configs(BaseModel):
    openai_key: str
    frontend_url: str
    azure_blob_storage_account_name: str = None
    azure_blob_storage_account_key: str = None
    azure_blob_storage_container_name: str = None
    azure_cosmos_db_url: str = None
    azure_cosmos_db_key: str = None
    azure_cosmos_db_database_name: str = None
    azure_cosmos_db_container_name: str = None
    sqlite3_db_path: str = None
    user_id: str = None
    swarm_id: str = None

class Platform(Enum):
    MAC = 'mac'    
    AZURE = 'azure'

class Swarm(BaseModel):
    root_path: str
    platform: Platform
    configs: Configs

    def get_memory(self, memory_id) -> Union[MemorySpaceMetadata, MemoryFolder]:
        pass    
    
    def get_state(self) -> SwarmState:
        pass
    
    def get_history(self) -> SwarmHistory:
        pass

    def get_memory_space_metadata(self) -> MemorySpaceMetadata:
        pass
