'''
This module contains functions to load resources from within the package.
'''
import json
from importlib import resources
from typing import Any, BinaryIO
import sqlite3

def get_internal_action_metadata(action_id: str) -> dict:
    return get_internal_sqlite3_value('aga_swarm/action', 'action_space_metadata', action_id)

def get_internal_memory_metadata(memory_id: str) -> dict:
    return get_internal_sqlite3_value('aga_swarm/memory', 'memory_space_metadata', memory_id)

def get_internal_util_metadata(util_id: str) -> dict:
    return get_internal_sqlite3_value('aga_swarm/utils', 'util_space_metadata', util_id)

def get_internal_sqlite3_value(path: str, category: str, key: str) -> dict:
    with resources.path(path, f'{category}.sqlite3') as db_path:
        try:
            with sqlite3.connect(str(db_path)) as conn:
                cursor = conn.cursor()
                cursor.execute('SELECT value FROM kv_store WHERE key = ?', (key,))
                result = cursor.fetchone()
                if result:
                    return result[0]
                else:
                    raise ValueError(f"Key: `{key}` does not exist in category {category}.")
        except Exception as e:
            raise ValueError(f'Failed to retrieve value from SQLite3: {str(e)}')

def get_json_data(package: str, resource_name: str) -> Any:
    with resources.open_text(package, resource_name) as file:
        return json.load(file)

def get_binary_data(package: str, resource_name: str) -> bytes:
    with resources.open_binary(package, resource_name) as file:
        return file.read()

def get_binary_file(package: str, resource_name: str) -> BinaryIO:
    return resources.open_binary(package, resource_name)
