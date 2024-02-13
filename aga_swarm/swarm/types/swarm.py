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
    mongodb_uri: str = None
    mongodb_db_name: str = None

class Platform(Enum):
    MAC = 'mac'    
    AZURE = 'azure'

class Swarm(BaseModel):
    root_path: str
    platform: Platform
    configs: Configs
