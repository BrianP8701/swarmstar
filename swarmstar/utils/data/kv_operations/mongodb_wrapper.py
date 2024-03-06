from __future__ import annotations

from typing import TYPE_CHECKING
from swarmstar.utils.data.kv_operations.mongodb import *

if TYPE_CHECKING:
    from swarmstar.types import SwarmConfig

def add_kv(swarm: SwarmConfig, collection_name: str, _id: str, value: dict) -> None:
    return mongodb_add_kv(swarm.mongodb_uri, swarm.mongodb_db_name, collection_name, _id, value)

def get_kv(swarm: SwarmConfig, collection_name: str, _id: str) -> dict:
    return mongodb_get_kv(swarm.mongodb_uri, swarm.mongodb_db_name, collection_name, _id)

def delete_kv(swarm: SwarmConfig, collection_name: str, _id: str) -> None:
    return mongodb_delete_kv(swarm.mongodb_uri, swarm.mongodb_db_name, collection_name, _id)

def update_kv(swarm: SwarmConfig, collection_name: str, _id: str, updated_values: dict) -> None:
    return mongodb_update_kv(swarm.mongodb_uri, swarm.mongodb_db_name, collection_name, _id, updated_values)

def set_kv(swarm: SwarmConfig, collection_name: str, _id: str, new_value: dict) -> None:
    return mongodb_set_kv(swarm.mongodb_uri, swarm.mongodb_db_name, collection_name, _id, new_value)

def append_to_list(swarm: SwarmConfig, collection_name: str, _id: str, key: str, value) -> None:
    return mongodb_append_to_list(swarm.mongodb_uri, swarm.mongodb_db_name, collection_name, _id, key, value)

def get_element_by_index(swarm: SwarmConfig, collection_name: str, _id: str, index: int) -> any:
    return mongodb_get_element_by_index(swarm.mongodb_uri, swarm.mongodb_db_name, collection_name, _id, index)

def get_list_length(swarm: SwarmConfig, collection_name: str, _id: str) -> int:
    return mongodb_get_list_length(swarm.mongodb_uri, swarm.mongodb_db_name, collection_name, _id)
