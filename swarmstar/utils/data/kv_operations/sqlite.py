'''
When the swarm object is created a single sqlite3 database is created for the swarm space.

This database is used to store all kv store data with the key being the category and the key.
'''
import sqlite3
import json

from swarmstar.models import SwarmConfig

def create_or_open_kv_db(db_path: str) -> None:
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute('CREATE TABLE IF NOT EXISTS kv_store (key TEXT PRIMARY KEY, value TEXT)')
        conn.commit()
    except Exception as e:
        raise ValueError(f'Failed to create or open kv store db: {str(e)}')

def upload_swarm_space_kv_pair(swarm: SwarmConfig, category: str, key: str, value: dict) -> None:
    try:
        conn = sqlite3.connect(swarm.configs.sqlite3_db_path)
        cursor = conn.cursor()
        key = f'{category}_{key}'
        if type(value) != str: value = json.dumps(value)        
        cursor.execute('INSERT OR REPLACE INTO kv_store (key, value) VALUES (?, ?)', (key, value))
        conn.commit()
    except Exception as e:
        raise ValueError(f'Failed to upload kv pair: {str(e)}')

def retrieve_swarm_space_kv_value(swarm: SwarmConfig, category: str, key: str) -> dict:
    try:
        conn = sqlite3.connect(swarm.configs.sqlite3_db_path)
        cursor = conn.cursor()
        key = f'{category}_{key}'
        cursor.execute('SELECT value FROM kv_store WHERE key = ?', (key,))
        result = cursor.fetchone()
        if result:
            
            return json.loads(result[0])
        raise ValueError(f'No value found for key: {key}')
    except Exception as e:
        raise ValueError(f'Failed to retrieve kv value: {str(e)} at {swarm.configs.sqlite3_db_path}')

def delete_swarm_space_kv_pair(swarm: SwarmConfig, category: str, key: str) -> None:
    try:
        conn = sqlite3.connect(swarm.configs.sqlite3_db_path)
        cursor = conn.cursor()
        key = f'{category}_{key}'
        cursor.execute('DELETE FROM kv_store WHERE key = ?', (key,))
        conn.commit()
    except Exception as e:
        raise ValueError(f'Failed to delete kv pair: {str(e)}')
