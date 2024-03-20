"""
This file provides methods to retrieve data internal to the swarmstar package.

Sources include the internal sqlite database and internal files.
"""
from typing import Dict, Any
import sqlite3
import json
from importlib import resources


def get_internal_sqlite(category: str, key: str) -> Dict[str, Any]:
    """
    Retrieves a key-value pair from the internal sqlite database.
    
    :param category: The table to retrieve the value from.
    :param key: The key to retrieve the value for.
    :return: The value for the key.
    """
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


def get_internal_file_as_string(file_name: str) -> str:
    """
    Retrieves the content of an internal file as a string.

    :param file_name: File should be in the swarmstar package.
    :return: The content of the file as a string.
    """
    try:
        with resources.open_text('swarmstar', file_name) as file:
            return file.read()
    except FileNotFoundError:
        raise ValueError(f'File {file_name} not found in package.')
    except Exception as e:
        raise ValueError(f'Failed to read file {file_name}: {str(e)}')
