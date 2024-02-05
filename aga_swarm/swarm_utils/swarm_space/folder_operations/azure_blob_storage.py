from azure.storage.blob import BlobServiceClient

from aga_swarm.swarm.types import Swarm

def delete_folder(swarm: Swarm, folder_path: str) -> dict:
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
        container_client.delete_blob(folder_path)
        print(f"Blob {folder_path} deleted from container {container_name}.")
    except Exception as e:
        print(f"An error occurred: {e}")
        return {'success': False, 'error_message': str(e)}
    return {'success': True, 'error_message': ''}

def list_folder(swarm: Swarm, folder_path: str) -> dict:
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

        # List the blobs in the container
        blob_list = container_client.list_blobs(name_starts_with=folder_path)
        print(f"Blobs in folder {folder_path}:")
        for blob in blob_list:
            print(blob.name)
    except Exception as e:
        print(f"An error occurred: {e}")
        return {'success': False, 'error_message': str(e)}
    return {'success': True, 'error_message': ''}

def make_folder(swarm: Swarm, folder_path: str) -> dict:
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

        # Create a blob
        container_client.upload_blob(name=folder_path)
        print(f"Blob {folder_path} created in container {container_name}.")
    except Exception as e:
        print(f"An error occurred: {e}")
        return {'success': False, 'error_message': str(e)}
    return {'success': True, 'error_message': ''}

def move_folder(swarm: Swarm, folder_path: str, new_folder_path: str) -> dict:
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
        blob_client = container_client.get_blob_client(folder_path)

        # Copy the blob
        blob_client.start_copy_from_url(new_folder_path)
        print(f"Blob {folder_path} copied to {new_folder_path} in container {container_name}.")
    except Exception as e:
        print(f"An error occurred: {e}")
        return {'success': False, 'error_message': str(e)}
    return {'success': True, 'error_message': ''}

def rename_folder(swarm: Swarm, folder_path: str, new_folder_name: str) -> dict:
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
        blob_client = container_client.get_blob_client(folder_path)

        # Rename the blob
        blob_client.rename_blob(new_folder_name)
        print(f"Blob {folder_path} renamed to {new_folder_name} in container {container_name}.")
    except Exception as e:
        print(f"An error occurred: {e}")
        return {'success': False, 'error_message': str(e)}
    return {'success': True, 'error_message': ''}
