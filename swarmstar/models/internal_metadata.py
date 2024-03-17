import sqlite3
import json
from importlib import resources


class SwarmstarInternal:
    """
        This class provides methods to read metadata from the 
        internal sqlite database.
    """
    @staticmethod
    def get_action_metadata(action_id: str) -> dict:
        return SwarmstarInternal.get_internal_sqlite("action_metadata_tree", action_id)

    @staticmethod
    def get_memory_metadata(memory_id: str) -> dict:
        return SwarmstarInternal.get_internal_sqlite("memory_metadata_tree", memory_id)

    @staticmethod
    def get_util_metadata(util_id: str) -> dict:
        return SwarmstarInternal.get_internal_sqlite("util_metadata_tree", util_id)

    @staticmethod
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
