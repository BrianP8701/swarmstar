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


def add_kv(swarm: SwarmConfig, category: str, key: str, value: dict) -> None:
    kv_operations_module = get_kv_operations_module(swarm)
    return kv_operations_module.add_kv(swarm, category, key, value)


def get_kv(swarm: SwarmConfig, category: str, key: str) -> dict:
    kv_operations_module = get_kv_operations_module(swarm)
    return kv_operations_module.get_kv(swarm, category, key)


def delete_kv(swarm: SwarmConfig, category: str, key: str) -> None:
    kv_operations_module = get_kv_operations_module(swarm)
    return kv_operations_module.delete_kv(swarm, category, key)


def update_kv(swarm: SwarmConfig, category: str, key: str, value: dict) -> None:
    kv_operations_module = get_kv_operations_module(swarm)
    return kv_operations_module.update_kv(swarm, category, key, value)
