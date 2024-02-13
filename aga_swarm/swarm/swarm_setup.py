'''
Swarm setup includes:
    1. Setting up storage for the swarm space on your chosen platform
    2. Creating a swarm object
    
The swarm space contains all the metadata for the swarm spaces, a stage
for generated content, a place to store the state of the swarm, and more.
    
The swarm object contains keys and configs for your personal swarm space. It's
passed around between every node and action. Keep it safe and private!
'''
import os

from aga_swarm.swarm.types import Swarm, Platform, Configs
from aga_swarm.utils.data.kv_operations.mongodb import restore_database, create_collection_with_unique_index
from aga_swarm.utils.data.kv_operations.main import upload_swarm_space_kv_pair

def setup_swarm_space(openai_key: str, frontend_url: str, root_path: str, platform: str, **kwargs) -> Swarm:
    try:
        platform = Platform(platform)
    except ValueError:
        raise ValueError(f'Invalid platform: {platform}')
    
    platform_map = {
        'mac': _setup_mac_swarm_space,
        'azure': _setup_azure_swarm_space,
    }
    
    swarm = platform_map[platform.value](openai_key, frontend_url, root_path, **kwargs)
    upload_swarm_space_kv_pair(swarm, 'swarm_history', 'current_frame', 0)
    upload_swarm_space_kv_pair(swarm, '', 'swarm', swarm.model_dump_json())
    return swarm
    
    

def _setup_mac_swarm_space(openai_key: str, frontend_url: str, root_path: str, **kwargs) -> Swarm:
    if os.path.exists(root_path):
        if os.listdir(root_path):
            raise ValueError(f'Root path folder must be empty: {root_path}')
    else:
        os.makedirs(root_path)
    
    # TODO - add the correct path
    restore_database('add the proper path', kwargs['mongodb_uri'], kwargs['mongodb_db_name'])
    
    return Swarm(
        swarm_space_root_path=root_path,
        platform=Platform.MAC,
        root_path=root_path,
        configs=Configs(
            openai_key=openai_key,
            frontend_url=frontend_url,
            mongodb_uri=kwargs['mongodb_uri'],
            mongodb_db_name=kwargs['mongodb_db_name']
        )
    )

def _setup_azure_swarm_space(openai_key: str, frontend_url: str, root_path: str, **kwargs) -> Swarm:
    # Test connection to Azure Blob Storage
    from azure.storage.blob import BlobServiceClient
    storage_account_name = kwargs['azure_blob_storage_account_name']
    storage_account_key = kwargs['azure_blob_storage_account_key']
    container_name = kwargs['azure_blob_storage_container_name']

    try:
        blob_service_client = BlobServiceClient(
            account_url=f"https://{storage_account_name}.blob.core.windows.net/",
            credential=storage_account_key
        )
    except Exception as e:
        raise ValueError(f'Failed to connect to Azure Blob Storage: {str(e)}')
    
    # Test connection to Azure CosmosDB
    from azure.cosmos import CosmosClient
    cosmos_db_url = kwargs['azure_cosmos_db_url']
    cosmos_db_key = kwargs['azure_cosmos_db_key']
    database_name = kwargs['azure_cosmos_db_database_name']
    container_name = kwargs['azure_cosmos_db_container_name']
    try:
        cosmos_client = CosmosClient(cosmos_db_url, credential=cosmos_db_key)
        database = cosmos_client.get_database_client(database_name)
        container = database.get_container_client(container_name)
    except Exception as e:
        raise ValueError(f'Failed to connect to Azure CosmosDB: {str(e)}')
    
    return Swarm(
        swarm_space_root_path=kwargs.get('root_path', None),
        platform=Platform.AZURE,
        root_path=root_path,
        configs=Configs(
            openai_key=openai_key,
            frontend_url=frontend_url,
            azure_blob_storage_account_name=kwargs['azure_blob_storage_account_name'],
            azure_blob_storage_account_key=kwargs['azure_blob_storage_account_key'],
            azure_blob_storage_container_name=kwargs['azure_blob_storage_container_name'],
            azure_cosmos_db_url=kwargs['azure_cosmos_db_url'],
            azure_cosmos_db_key=kwargs['azure_cosmos_db_key'],
            azure_cosmos_db_database_name=kwargs['azure_cosmos_db_database_name'],
            azure_cosmos_db_container_name=kwargs.get('azure_cosmos_db_container_name'),
        )
    )

