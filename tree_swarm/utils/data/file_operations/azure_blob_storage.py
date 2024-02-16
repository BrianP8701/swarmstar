from __future__ import annotations
from typing import TYPE_CHECKING
from azure.storage.blob import BlobServiceClient

if TYPE_CHECKING:
    from tree_swarm.swarm.types import Swarm

def delete_file(swarm: Swarm, file_path: str) -> None:
    storage_account_name = swarm.configs.azure_blob_storage_account_name
    storage_account_key = swarm.configs.azure_blob_storage_account_key
    container_name = swarm.configs.azure_blob_storage_container_name
    
    try:
        # Create a blob service client
        blob_service_client = BlobServiceClient(
            account_url=f"https://{storage_account_name}.blob.core.windows.net/",
            credential=storage_account_key
        )

        # Get a client to interact with the specified container
        container_client = blob_service_client.get_container_client(container_name)

        # Delete the blob
        container_client.delete_blob(file_path)
    except Exception as e:
        raise ValueError(f'Failed to delete file: {str(e)}')
    
def move_file(swarm: Swarm, file_path: str, new_file_path: str) -> None:
    storage_account_name = swarm.configs.azure_blob_storage_account_name
    storage_account_key = swarm.configs.azure_blob_storage_account_key
    container_name = swarm.configs.azure_blob_storage_container_name
    
    try:
        # Create a blob service client
        blob_service_client = BlobServiceClient(
            account_url=f"https://{storage_account_name}.blob.core.windows.net/",
            credential=storage_account_key
        )

        # Get a client to interact with the specified container
        container_client = blob_service_client.get_container_client(container_name)

        # Get a blob client to interact with the specified blob
        blob_client = container_client.get_blob_client(file_path)

        # Copy the blob
        blob_client.start_copy_from_url(new_file_path)
    except Exception as e:
        raise ValueError(f'Failed to move file: {str(e)}')
    
def rename_file(swarm: Swarm, file_path: str, new_file_name: str) -> None:
    storage_account_name = swarm.configs.azure_blob_storage_account_name
    storage_account_key = swarm.configs.azure_blob_storage_account_key
    container_name = swarm.configs.azure_blob_storage_container_name
    
    try: 
        # Create a blob service client
        blob_service_client = BlobServiceClient(
            account_url=f"https://{storage_account_name}.blob.core.windows.net/",
            credential=storage_account_key
        )

        # Get a client to interact with the specified container
        container_client = blob_service_client.get_container_client(container_name)

        # Get a blob client to interact with the specified blob
        blob_client = container_client.get_blob_client(file_path)

        # Rename the blob
        blob_client.rename_blob(new_file_name)
    except Exception as e:
        raise ValueError(f'Failed to rename file: {str(e)}')

def upload_file(swarm: Swarm, file_path: str, file_bytes: bytes) -> None:
    storage_account_name = swarm.configs.azure_blob_storage_account_name
    storage_account_key = swarm.configs.azure_blob_storage_account_key
    container_name = swarm.configs.azure_blob_storage_container_name
    
    try:
        # Create a blob service client
        blob_service_client = BlobServiceClient(
            account_url=f"https://{storage_account_name}.blob.core.windows.net/",
            credential=storage_account_key
        )

        # Get a client to interact with the specified container
        container_client = blob_service_client.get_container_client(container_name)

        # Create the container if it does not exist
        container_client.create_container()

        # Get a blob client to interact with the specified blob
        blob_client = container_client.get_blob_client(file_path)

        # Upload the file
        blob_client.upload_blob(file_bytes, overwrite=True)
    except Exception as e:
        raise ValueError(f'Failed to upload file: {str(e)}')

def retrieve_file(swarm: Swarm, file_path: str) -> bytes:
    storage_account_name = swarm.configs.azure_blob_storage_account_name
    storage_account_key = swarm.configs.azure_blob_storage_account_key
    container_name = swarm.configs.azure_blob_storage_container_name
    
    try:
        # Create a blob service client
        blob_service_client = BlobServiceClient(
            account_url=f"https://{storage_account_name}.blob.core.windows.net/",
            credential=storage_account_key
        )

        # Get a client to interact with the specified container
        container_client = blob_service_client.get_container_client(container_name)

        # Get a blob client to interact with the specified blob
        blob_client = container_client.get_blob_client(file_path)

        # Download the blob
        return blob_client.download_blob().readall()
        
    except Exception as e:
        raise ValueError(f'Failed to retrieve file: {str(e)}')
