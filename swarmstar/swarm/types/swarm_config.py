'''
Use this object to configure the swarm to your platform and personal preferences.
'''

from pydantic import BaseModel
from typing_extensions import Literal
from typing import Union, Optional

class SwarmConfig(BaseModel):
    root_path: str
    openai_key: str
    platform: Literal['mac', 'azure']
    user_id: Optional[str] = None
    swarm_id: Optional[str] = None
    azure_blob_storage_account_name: Optional[str] = None
    azure_blob_storage_account_key: Optional[str] = None
    azure_blob_storage_container_name: Optional[str] = None
    azure_cosmos_db_url: Optional[str] = None
    azure_cosmos_db_key: Optional[str] = None
    azure_cosmos_db_database_name: Optional[str] = None
    azure_cosmos_db_container_name: Optional[str] = None
    mongodb_uri: Optional[str] = None
    mongodb_db_name: Optional[str] = None
    
class PlatformConfig(BaseModel):
    platform: Literal['mac', 'azure']

class AzureConfig(PlatformConfig):
    platform: Literal['azure']
    user_id: str
    swarm_id: str
    azure_blob_storage_account_name: str = None
    azure_blob_storage_account_key: str = None
    azure_blob_storage_container_name: str = None
    azure_cosmos_db_url: str = None
    azure_cosmos_db_key: str = None
    azure_cosmos_db_database_name: str = None
    azure_cosmos_db_container_name: str = None
    
class LocalConfig(PlatformConfig):
    platform: Literal['mac']
    mongodb_uri: str = None
    mongodb_db_name: str = None