"""
Use this object to configure the swarm to your platform and personal preferences.
"""

from typing import Optional, Dict, Any

from pydantic import BaseModel, model_serializer, Field
from typing_extensions import Literal

from swarmstar.utils.misc.generate_uuid import generate_uuid

class SwarmConfig(BaseModel):
    id: Optional[str] = Field(default_factory=lambda: generate_uuid('config'))
    swarm_id: Optional[str] = None
    root_path: str
    openai_key: str
    platform: Literal["mac", "azure"]
    user_id: Optional[str] = None
    azure_blob_storage_account_name: Optional[str] = None
    azure_blob_storage_account_key: Optional[str] = None
    azure_blob_storage_container_name: Optional[str] = None
    azure_cosmos_db_url: Optional[str] = None
    azure_cosmos_db_key: Optional[str] = None
    azure_cosmos_db_database_name: Optional[str] = None
    azure_cosmos_db_container_name: Optional[str] = None
    mongodb_uri: Optional[str] = None
    mongodb_db_name: Optional[str] = None
    kv_operations_path: Optional[str] = None
    folder_operations_path: Optional[str] = None
    file_operations_path: Optional[str] = None
    
    @model_serializer
    def serialize_model(self) -> Dict[str, Any]:
        return {k: v for k, v in dict(self).items() if v is not None}


# The types below aren't actually used in the codebase, but they are used in the documentation.


class PlatformConfig(BaseModel):
    platform: Literal["mac", "azure"]

class AzureConfig(PlatformConfig):
    platform: Literal["azure"]
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
    platform: Literal["mac"]
    mongodb_uri: str = None
    mongodb_db_name: str = None
