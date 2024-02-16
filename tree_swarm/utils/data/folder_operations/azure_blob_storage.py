'''
Azure Blob Storage doesen't have a concept of folders. It has a flat
structure and uses the '/' character in the blob name to simulate a folder.

For a common interface to folder operations I've still implemented these, but
make_folder() does nothing and rename_folder() and move_folder() are the
same thing.
'''
from __future__ import annotations
from typing import TYPE_CHECKING, List
from azure.storage.blob import BlobServiceClient

if TYPE_CHECKING:
    from tree_swarm.swarm.types import Swarm

def delete_folder(swarm: Swarm, folder_path: str) -> dict:
    try:
        blob_service_client = BlobServiceClient(
            account_url=f"https://{swarm.configs.azure_blob_storage_account_name}.blob.core.windows.net/",
            credential=swarm.configs.azure_blob_storage_account_key
        )
        container_client = blob_service_client.get_container_client(swarm.configs.azure_blob_storage_container_name)

        blobs_list = list(container_client.list_blobs(name_starts_with=folder_path))
        for blob in blobs_list:
            container_client.delete_blob(blob.name)
    except Exception as e:
        raise ValueError(f'Failed to delete folder: {str(e)}')

def list_folder(swarm: Swarm, folder_path: str) -> List[str]:
    try:
        blob_service_client = BlobServiceClient(
            account_url=f"https://{swarm.configs.azure_blob_storage_account_name}.blob.core.windows.net/",
            credential=swarm.configs.azure_blob_storage_account_key
        )
        container_client = blob_service_client.get_container_client(swarm.configs.azure_blob_storage_container_name)

        # Ensure folder_path ends with a '/' to properly simulate a folder structure
        if not folder_path.endswith('/'):
            folder_path += '/'

        blob_list = container_client.list_blobs(name_starts_with=folder_path)
        paths = []
        for blob in blob_list:
            # Split the blob name by '/' and filter out those that are more than one level deep
            if blob.name[len(folder_path):].count('/') == 0:
                paths.append(blob.name)
    except Exception as e:
        raise ValueError(f'Failed to list folder: {str(e)}')

def make_folder(swarm: Swarm, folder_path: str) -> None:
    return None

def move_folder(swarm: Swarm, folder_path: str, new_folder_name: str) -> None:
    try:
        rename_folder(swarm, folder_path, new_folder_name)
    except Exception as e:
        raise ValueError(f'Failed to move folder: {str(e)}')

def rename_folder(swarm: Swarm, folder_path: str, new_folder_path: str) -> None:
    try:
        blob_service_client = BlobServiceClient(
            account_url=f"https://{swarm.configs.azure_blob_storage_account_name}.blob.core.windows.net/",
            credential=swarm.configs.azure_blob_storage_account_key
        )
        container_client = blob_service_client.get_container_client(swarm.configs.azure_blob_storage_container_name)

        blobs = list(container_client.list_blobs(name_starts_with=folder_path))
        for blob in blobs:
            # Construct the new blob name
            new_blob_name = new_folder_path + blob.name[len(folder_path):]

            # Copy the blob to the new location
            copied_blob = container_client.get_blob_client(new_blob_name)
            copied_blob.start_copy_from_url(blob.url)

            container_client.delete_blob(blob.name)
    except Exception as e:
        raise ValueError(f'Failed to rename folder: {str(e)}')
    
