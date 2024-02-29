"""
This module contains functions to load resources from within the package.
"""
import json
import sqlite3
from importlib import resources
from typing import Any, BinaryIO

from swarmstar.swarm.types.swarm_config import SwarmConfig
from swarmstar.utils.data.kv_operations.main import get_kv

def get_internal_action_metadata(action_id: str) -> dict:
    return get_internal_sqlite_kv("action_space", action_id)


def get_internal_memory_metadata(memory_id: str) -> dict:
    return get_internal_sqlite_kv("memory_space", memory_id)


def get_internal_util_metadata(util_id: str) -> dict:
    return get_internal_sqlite_kv("util_space", util_id)


def get_internal_sqlite_kv(category: str, key: str) -> dict:
    try:
        with resources.path('swarmstar.internal_metadata', f'{category}.sqlite3') as db_path:
            conn = sqlite3.connect(str(db_path))
            cursor = conn.cursor()
            key = key
            cursor.execute('SELECT value FROM kv_store WHERE key = ?', (key,))
            result = cursor.fetchone()
            if result:
                return json.loads(result[0])
            else:
                raise ValueError(f'No value found for key: {key}')
    except Exception as e:
        raise ValueError(f'Failed to retrieve kv value: {str(e)} at {db_path}')

def get_json_data(package: str, resource_name: str) -> Any:
    with resources.open_text(package, resource_name) as file:
        return json.load(file)


def get_binary_data(package: str, resource_name: str) -> bytes:
    with resources.open_binary(package, resource_name) as file:
        return file.read()


def get_binary_file(package: str, resource_name: str) -> BinaryIO:
    return resources.open_binary(package, resource_name)
