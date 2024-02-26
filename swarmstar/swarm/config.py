"""
Swarm setup includes:
    1. Setting up storage for the swarm space on your chosen platform
    2. Creating a swarm object
    
The swarm space contains all the metadata for the swarm spaces, a stage
for generated content, a place to store the state of the swarm, and more.
    
The swarm object contains keys and configs for your personal swarm space. It's
passed around between every node and action. Keep it safe and private!
"""
import os

from swarmstar.swarm.types import SwarmConfig
from swarmstar.utils.data.kv_operations.main import add_kv
from swarmstar.utils.data.kv_operations.mongodb import (
    check_and_create_database,
    restore_database,
)

def configure_swarm(
    openai_key: str, root_path: str, platform: str, **kwargs
) -> SwarmConfig:
    try:
        if platform not in ["mac", "azure"]:
            raise ValueError
    except ValueError:
        raise ValueError(f"Invalid platform: {platform}")

    platform_map = {
        "mac": _setup_mac_swarm_space,
        "azure": _setup_azure_swarm_space,
    }

    swarm = platform_map[platform](openai_key, root_path, **kwargs)
    add_kv(swarm, "swarm_history", "current_frame", {"frame": 0})
    add_kv(swarm, "swarm", "swarm", swarm.model_dump())
    return swarm


def _setup_mac_swarm_space(openai_key: str, root_path: str, **kwargs) -> SwarmConfig:
    required_keys = ["mongodb_uri", "mongodb_db_name"]
    missing_keys = [key for key in required_keys if key not in kwargs]
    if missing_keys:
        raise ValueError(f'Missing required key(s): {", ".join(missing_keys)}')

    if os.path.exists(root_path):
        if os.listdir(root_path):
            raise ValueError(f"Root path folder must be empty: {root_path}")
    else:
        os.makedirs(root_path)

    check_and_create_database(kwargs["mongodb_uri"], kwargs["mongodb_db_name"])
    restore_database(
        "swarmstar/internal_metadata", kwargs["mongodb_uri"], kwargs["mongodb_db_name"]
    )
    return SwarmConfig(
        openai_key=openai_key,
        root_path=root_path,
        platform="mac",
        mongodb_uri=kwargs["mongodb_uri"],
        mongodb_db_name=kwargs["mongodb_db_name"],
    )


def _setup_azure_swarm_space(openai_key: str, root_path: str, **kwargs) -> SwarmConfig:
    # Test connection to Azure Blob Storage
    from azure.storage.blob import BlobServiceClient

    storage_account_name = kwargs["azure_blob_storage_account_name"]
    storage_account_key = kwargs["azure_blob_storage_account_key"]
    container_name = kwargs["azure_blob_storage_container_name"]

    try:
        blob_service_client = BlobServiceClient(
            account_url=f"https://{storage_account_name}.blob.core.windows.net/",
            credential=storage_account_key,
        )
    except Exception as e:
        raise ValueError(f"Failed to connect to Azure Blob Storage: {str(e)}")

    # Test connection to Azure CosmosDB
    from azure.cosmos import CosmosClient

    cosmos_db_url = kwargs["azure_cosmos_db_url"]
    cosmos_db_key = kwargs["azure_cosmos_db_key"]
    database_name = kwargs["azure_cosmos_db_database_name"]
    container_name = kwargs["azure_cosmos_db_container_name"]
    try:
        cosmos_client = CosmosClient(cosmos_db_url, credential=cosmos_db_key)
        database = cosmos_client.get_database_client(database_name)
        database.get_container_client(container_name)
    except Exception as e:
        raise ValueError(f"Failed to connect to Azure CosmosDB: {str(e)}")

    return SwarmConfig(
        openai_key=openai_key,
        root_path=root_path,
        platform="azure",
        user_id=kwargs["user_id"],
        swarm_id=kwargs["swarm_id"],
        azure_blob_storage_account_name=kwargs["azure_blob_storage_account_name"],
        azure_blob_storage_account_key=kwargs["azure_blob_storage_account_key"],
        azure_blob_storage_container_name=kwargs["azure_blob_storage_container_name"],
        azure_cosmos_db_url=kwargs["azure_cosmos_db_url"],
        azure_cosmos_db_key=kwargs["azure_cosmos_db_key"],
        azure_cosmos_db_database_name=kwargs["azure_cosmos_db_database_name"],
        azure_cosmos_db_container_name=kwargs.get("azure_cosmos_db_container_name"),
    )
