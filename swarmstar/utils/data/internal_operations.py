"""
This module contains functions to load resources from within the package.
"""
import json
from importlib import resources
from typing import Any, BinaryIO

from swarmstar.swarm.types.swarm_config import SwarmConfig
from swarmstar.utils.data.kv_operations.main import get_kv


def get_internal_action_metadata(swarm: SwarmConfig, action_id: str) -> dict:
    return get_internal_mongodb_value(swarm, "action_space", action_id)


def get_internal_memory_metadata(swarm: SwarmConfig, memory_id: str) -> dict:
    return get_internal_mongodb_value(swarm, "memory_space", memory_id)


def get_internal_util_metadata(swarm: SwarmConfig, util_id: str) -> dict:
    return get_internal_mongodb_value(swarm, "util_space", util_id)


def get_internal_mongodb_value(swarm: SwarmConfig, category: str, key: str) -> dict:
    get_kv(swarm, category, key)


def get_json_data(package: str, resource_name: str) -> Any:
    with resources.open_text(package, resource_name) as file:
        return json.load(file)


def get_binary_data(package: str, resource_name: str) -> bytes:
    with resources.open_binary(package, resource_name) as file:
        return file.read()


def get_binary_file(package: str, resource_name: str) -> BinaryIO:
    return resources.open_binary(package, resource_name)
