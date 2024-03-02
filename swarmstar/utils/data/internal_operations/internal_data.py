import json
from importlib import resources
from typing import Any, BinaryIO
import sqlite3
from importlib import resources
import json

def get_json_data(package: str, resource_name: str) -> Any:
    with resources.open_text(package, resource_name) as file:
        return json.load(file)

def get_binary_data(package: str, resource_name: str) -> bytes:
    with resources.open_binary(package, resource_name) as file:
        return file.read()

def get_binary_file(package: str, resource_name: str) -> BinaryIO:
    return resources.open_binary(package, resource_name)

def get_internal_metadata(category: str, key: str) -> dict:
    try:
        with resources.path('swarmstar', f'internal_metadata.sqlite3') as db_path:
            conn = sqlite3.connect(str(db_path))
            cursor = conn.cursor()
            key = key
            cursor.execute(f'SELECT value FROM {category} WHERE _id = ?', (key,))
            result = cursor.fetchone()
            if result:
                result = json.loads(result[0])
                result['id'] = key
                return result
            else:
                raise ValueError(f'No value found for key: {key}')
    except Exception as e:
        raise ValueError(f'Failed to retrieve kv value: {str(e)} at {db_path}')
