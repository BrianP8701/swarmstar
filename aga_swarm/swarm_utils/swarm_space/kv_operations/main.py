'''
This is a common interface to KV stores for the swarm space.

Things like action space, util space and memory space metadata, swarm state
and more will be stored in KV stores.
'''

from typing import Any
from importlib import import_module
from aga_swarm.swarm.types import Swarm

platform_map = {
    'local': 'aga_swarm.swarm_utils.swarm_space.kv_operations.sqlite3',
    'azure': 'aga_swarm.swarm_utils.swarm_space.kv_operations.cosmos_db',
}

def upload_swarm_space_kv_pair(swarm: Swarm, category: str, key: str, value: dict):
    platform = swarm.platform.value
    kv_operations_module = import_module(platform_map[platform])
    return kv_operations_module.upload_swarm_space_kv_pair(swarm, category, key, value)

def retrieve_swarm_space_kv_value(swarm: Swarm, category: str, key: str):
    platform = swarm.platform.value
    kv_operations_module = import_module(platform_map[platform])
    return kv_operations_module.retrieve_swarm_space_kv_value(swarm, category, key)

def delete_swarm_space_kv_pair(swarm: Swarm, category: str, key: str):
    platform = swarm.platform.value
    kv_operations_module = import_module(platform_map[platform])
    return kv_operations_module.delete_swarm_space_kv_document(swarm, category, key)
