'''
This is a common interface to KV stores for the swarm space.

Things like action space, util space and memory space metadata, swarm state
and more will be stored in KV stores.
'''

from typing import Any
from importlib import import_module
from aga_swarm.swarm.types import Swarm

platform_map = {
    'local': 'aga_swarm.swarm_utils.swarm_space.kv_operations.cosmos_db',
    'azure': 'aga_swarm.swarm_utils.swarm_space.kv_operations.level_db'
}

def upload_swarm_space_kv_document(swarm: Swarm, category: str, key: str, document: Any):
    platform = swarm.platform.value
    kv_operations_module = import_module(platform_map[platform])
    return kv_operations_module.upload_swarm_space_kv_document(swarm, category, key, document)

def retrieve_swarm_space_kv_document(swarm: Swarm, category: str, key: str):
    platform = swarm.platform.value
    kv_operations_module = import_module(platform_map[platform])
    return kv_operations_module.retrieve_swarm_space_kv_document(swarm, category, key)

def delete_swarm_space_kv_document(swarm: Swarm, category: str, key: str):
    platform = swarm.platform.value
    kv_operations_module = import_module(platform_map[platform])
    return kv_operations_module.delete_swarm_space_kv_document(swarm, category, key)
