"""
This is a common interface to KV stores for the swarm space.

Things like action, util and memory space metadata, swarm state, 
swarm history and more will be stored in KV stores.
"""
from __future__ import annotations

from importlib import import_module
from typing import TYPE_CHECKING

from swarmstar.utils.data.external_operations.imports import import_module_from_path

if TYPE_CHECKING:
    from swarmstar.swarm.types.swarm_config import SwarmConfig


platform_map = {
    "mac": "swarmstar.utils.data.kv_operations.mongodb",
    "azure": "swarmstar.utils.data.kv_operations.cosmos_db",
}

def get_kv_operations_module(swarm: SwarmConfig):
    if swarm.kv_operations_path:
        return import_module_from_path('kv_operations_module', swarm.kv_operations_path)
    else:
        platform = swarm.platform
        return import_module(platform_map[platform])


def add_kv(swarm: SwarmConfig, category: str, _id: str, value: dict) -> None:
    kv_operations_module = get_kv_operations_module(swarm)
    return kv_operations_module.add_kv(swarm, category, _id, value)


def get_kv(swarm: SwarmConfig, category: str, _id: str) -> dict:
    kv_operations_module = get_kv_operations_module(swarm)
    return kv_operations_module.get_kv(swarm, category, _id)


def delete_kv(swarm: SwarmConfig, category: str, _id: str) -> None:
    kv_operations_module = get_kv_operations_module(swarm)
    return kv_operations_module.delete_kv(swarm, category, _id)


def update_kv(swarm: SwarmConfig, category: str, _id: str, value: dict) -> None:
    kv_operations_module = get_kv_operations_module(swarm)
    return kv_operations_module.update_kv(swarm, category, _id, value)

def set_kv(swarm: SwarmConfig, category: str, _id: str, value: dict) -> None:
    kv_operations_module = get_kv_operations_module(swarm)
    return kv_operations_module.set_kv(swarm, category, _id, value)

def append_to_list(swarm: SwarmConfig, category: str, _id: str, key: str, value: dict) -> None:
    kv_operations_module = get_kv_operations_module(swarm)
    return kv_operations_module.append_to_list(swarm, category, _id, key, value)

def get_element_by_index(swarm: SwarmConfig, category: str, _id: str, index: int) -> dict:
    kv_operations_module = get_kv_operations_module(swarm)
    return kv_operations_module.get_element_by_index(swarm, category, _id, index)

def get_list_length(swarm: SwarmConfig, category: str, _id: str) -> int:
    kv_operations_module = get_kv_operations_module(swarm)
    return kv_operations_module.get_list_length(swarm, category, _id)