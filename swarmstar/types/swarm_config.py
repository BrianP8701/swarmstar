"""
Use this object to configure the swarm to your platform and personal preferences.
"""

from typing import Optional, Dict, Any

from pydantic import BaseModel, model_serializer
from typing_extensions import Literal


class SwarmConfig(BaseModel):
    id: str
    root_path: Optional[str] = None # Set this on spawn
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
