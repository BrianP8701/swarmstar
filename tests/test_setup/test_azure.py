import os
import pytest
from dotenv import load_dotenv

from aga_swarm.swarm.swarm_setup import setup_swarm_space

@pytest.mark.azure
def test_setup_swarm_space():
    load_dotenv()
    # GEt openai key from env
    openai_key = os.environ.get('OPENAI_API_KEY')
    # get all values from .env
    azure_cosmos_db_url = os.environ.get('AZURE_COSMOS_DB_URL')
    azure_cosmos_db_key = os.environ.get('AZURE_COSMOS_DB_KEY')
    azure_cosmos_db_database_name = os.environ.get('AZURE_COSMOS_DB_DATABASE_NAME')
    azure_cosmos_db_container_name = os.environ.get('AZURE_COSMOS_DB_CONTAINER_NAME')
    azure_blob_storage_account_name = os.environ.get('AZURE_BLOB_STORAGE_ACCOUNT_NAME')
    azure_blob_storage_account_key = os.environ.get('AZURE_BLOB_STORAGE_ACCOUNT_KEY')
    azure_blob_storage_container_name = os.environ.get('AZURE_BLOB_STORAGE_CONTAINER_NAME')
    setup_swarm_space(openai_key, 'blank for now', 'testing/test1/', 'azure', azure_cosmos_db_url=azure_cosmos_db_url, azure_cosmos_db_key=azure_cosmos_db_key, azure_cosmos_db_database_name=azure_cosmos_db_database_name, azure_cosmos_db_container_name=azure_cosmos_db_container_name, azure_blob_storage_account_name=azure_blob_storage_account_name, azure_blob_storage_account_key=azure_blob_storage_account_key, azure_blob_storage_container_name=azure_blob_storage_container_name)
