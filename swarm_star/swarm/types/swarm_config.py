'''
Use this object to configure the swarm to your platform and personal preferences.
'''

from pydantic import BaseModel
from typing_extensions import Literal

class SwarmConfig(BaseModel):
    root_path: str
    openai_key: str
    platform_config: 'PlatformConfig'

class PlatformConfig(BaseModel):
    platform: Literal['mac', 'azure']

class AzureConfig(PlatformConfig):
    platform: Literal['azure']
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