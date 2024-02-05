'''
When the swarm object is created a single sqlite3 database is created for the swarm space.

This database is used to store all kv store data with the key being the category and the key.
'''
from typing import Any
import sqlite3
import json

from aga_swarm.swarm.types import Swarm
from aga_swarm.swarm_utils.swarm_space.paths import validate_and_adjust_swarm_space_path

def create_or_open_kv_db(db_path: str):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('CREATE TABLE IF NOT EXISTS kv_store (key TEXT PRIMARY KEY, value TEXT)')
    conn.commit()
    return conn

def upload_swarm_space_kv_pair(swarm: Swarm, category: str, key: str, value: dict):
    conn = sqlite3.connect(swarm)
    cursor = conn.cursor()
    key = f'{category}_{key}'
    value = json.dumps(value)
    cursor.execute('INSERT OR REPLACE INTO kv_store (key, value) VALUES (?, ?)', (key, value))
    conn.commit()

def retrieve_swarm_space_kv_value(swarm: Swarm, category: str, key: str) -> dict:
    conn = sqlite3.connect(swarm.sqlite3_db_path)
    cursor = conn.cursor()
    key = f'{category}_{key}'
    cursor.execute('SELECT value FROM kv_store WHERE key = ?', (key,))
    result = cursor.fetchone()
    if result:
        return json.loads(result[0])
    return None

def delete_swarm_space_kv_pair(swarm: Swarm, category: str, key: str):
    conn = sqlite3.connect(swarm.sqlite3_db_path)
    cursor = conn.cursor()
    key = f'{category}_{key}'
    cursor.execute('DELETE FROM kv_store WHERE key = ?', (key,))
    conn.commit()
