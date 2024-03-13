import sqlite3
from importlib import resources
import json

def get_internal_sqlite(category: str, key: str) -> dict:
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
