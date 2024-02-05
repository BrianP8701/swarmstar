from azure.storage.blob import BlobServiceClient

from aga_swarm.swarm.types import Swarm

def delete_file(swarm: Swarm, file_path: str) -> dict:
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
        print(f"Blob {file_path} deleted from container {container_name}.")
    except Exception as e:
        print(f"An error occurred: {e}")
        return {'success': False, 'error_message': str(e)}
    return {'success': True, 'error_message': ''}
    
def move_file(swarm: Swarm, file_path: str, new_file_path: str) -> dict:
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
        print(f"Blob {file_path} copied to {new_file_path} in container {container_name}.")
    except Exception as e:
        print(f"An error occurred: {e}")
        return {'success': False, 'error_message': str(e)}
    return {'success': True, 'error_message': ''}
    
def rename_file(swarm: Swarm, file_path: str, new_file_name: str) -> dict:
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
        print(f"Blob {file_path} renamed to {new_file_name} in container {container_name}.")
    except Exception as e:
        print(f"An error occurred: {e}")
        return {'success': False, 'error_message': str(e)}
    return {'success': True, 'error_message': ''}

def upload_file(swarm: Swarm, file_path: str, file_bytes: bytes) -> dict:
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
        print(f"File uploaded to blob {file_path} in container {container_name}.")
    except Exception as e:
        print(f"An error occurred: {e}")
        return {'success': False, 'error_message': str(e)}
    return {'success': True, 'error_message': ''}

def retrieve_file(swarm: Swarm, file_path: str) -> dict:
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
        file_bytes = blob_client.download_blob().readall()
        print(f"Blob {file_path} downloaded from container {container_name}.")
    except Exception as e:
        print(f"An error occurred: {e}")
        return {'success': False, 'error_message': str(e), 'data': None}
    return {'success': True, 'error_message': '', 'data': file_bytes}
