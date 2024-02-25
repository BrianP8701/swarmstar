"""
A single container is used for all operations for all users.

CosmosDB automatically splits the container into physical partitions and does all the scaling.
We just need to choose 3 logical partitions and have an id field for retrieval.

The swarm object will hold 2 of the partiton keys and the keys to get the swarm container.

Partition keys: user_id/swarm_id/category
"category" can be "action_space_metadata", "util_space_metadata", "memory_space_metadata", "swarm_state" etc.

The "id" field will be the key for the document.
"id" might be like "action_id", "util_id", "memory_id", "node_id" etc.

In this manner we have good logical partitions and can provide a standard interface for all KV operations.

For now cosmosdb python sdk doesen't support hierarchical partitions. So we'll append all the
partition keys into a single string and use it as the partition key and id for now
"""
from __future__ import annotations

from typing import TYPE_CHECKING

from azure.cosmos import CosmosClient

if TYPE_CHECKING:
    from swarmstar.swarm.types import SwarmConfig


def get_container(swarm: SwarmConfig, category: str):
    try:
        url = swarm.azure_cosmos_db_url
        cosmos_key = swarm.azure_cosmos_db_key
        container_name = swarm.azure_cosmos_db_container_name
        client = CosmosClient(url, credential=cosmos_key)
        database_name = client.get_database_client(swarm.azure_cosmos_db_database_name)
        container = database_name.get_container_client(container_name)
        return container
    except Exception as e:
        raise ValueError(f"Failed to connect to cosmosdb: {str(e)}") from e


def build_id(swarm: SwarmConfig, category: str, key: str) -> str:
    return f"{swarm.user_id}_{swarm.swarm_id}_{category}_{key}"


def add_kv(swarm: SwarmConfig, category: str, key: str, value: dict) -> None:
    container = get_container(swarm, category)

    id = build_id(swarm, category, key)
    value["id"] = id

    try:
        container.upsert_item(value)
    except Exception as e:
        raise ValueError(f"Failed to upload to cosmosdb: {str(e)}") from e


def get_kv(swarm: SwarmConfig, category: str, key: str):
    container = get_container(swarm, category)
    id = build_id(swarm, category, key)
    try:
        document = container.read_item(item=id, partition_key=id)
        return document
    except Exception as e:
        raise ValueError(f"Failed to retrieve from cosmosdb: {str(e)}") from e


def delete_kv(swarm: SwarmConfig, category: str, key: str):
    container = get_container(swarm, category)
    id = build_id(swarm, category, key)

    try:
        container.delete_item(item=id, partition_key=id)
    except Exception as e:
        raise ValueError(f"Failed to delete from cosmosdb: {str(e)}") from e


def update_kv(swarm: SwarmConfig, category: str, key: str, value: dict) -> None:
    container = get_container(swarm, category)
    build_id(swarm, category, key)

    try:
        container.upsert_item(value)
    except Exception as e:
        raise ValueError(f"Failed to update in cosmosdb: {str(e)}") from e


"""
The following works with a container that uses hierarchical partitions.
/ Partition keys: user_id/swarm_id/category
with id as the key for the document.
"""
# def add_kv(swarm: Swarm, category: str, key: str, value: dict):
#     url = swarm.azure_cosmos_db_url
#     cosmos_key = swarm.azure_cosmos_db_key
#     container_name = swarm.azure_cosmos_db_container_name
#     client = CosmosClient(url, credential=cosmos_key)
#     database_name = client.get_database_client(swarm.azure_cosmos_db_database_name)
#     container = database_name.get_container_client(container_name)

#     # Add partiton keys and id field. CosmosDB expects all values to be inside the dict.
#     value['id'] = key
#     value['category'] = category
#     value['user_id'] = swarm.user_id
#     value['swarm_id'] = swarm.swarm_id

#     try:
#         container.upsert_item(value)
#         return {'success': True, 'error_message': ''}
#     except Exception as e:
#         return {'success': False, 'error_message': str(e)}

# def get_kv(swarm: Swarm, category: str, key: str):
#     url = swarm.azure_cosmos_db_url
#     cosmos_key = swarm.azure_cosmos_db_key
#     container_name = swarm.azure_cosmos_db_container_name
#     client = CosmosClient(url, credential=cosmos_key)
#     database_name = client.get_database_client(swarm.azure_cosmos_db_database_name)
#     container = database_name.get_container_client(container_name)
#     partition_key = f'{swarm.user_id}/{swarm.swarm_id}/{category}'
#     partition_key = PartitionKey(partition_key)

#     try:
#         document = container.read_item(item=key, partition_key=key)
#         return {'success': True, 'error_message': '', 'data': document}
#     except Exception as e:
#         return {'success': False, 'error_message': str(e)}

# def delete_kv(swarm: Swarm, category: str, key: str):
#     url = swarm.azure_cosmos_db_url
#     cosmos_key = swarm.azure_cosmos_db_key
#     container_name = swarm.azure_cosmos_db_container_name
#     client = CosmosClient(url, credential=cosmos_key)
#     database_name = client.get_database_client(swarm.azure_cosmos_db_database_name)
#     container = database_name.get_container_client(container_name)
#     partition_key = f'{swarm.user_id}/{swarm.swarm_id}/{category}'
#     partition_key = PartitionKey(partition_key)

#     try:
#         container.delete_item(item=key, partition_key=key)
#         return {'success': True, 'error_message': ''}
#     except Exception as e:
#         return {'success': False, 'error_message': str(e)}
