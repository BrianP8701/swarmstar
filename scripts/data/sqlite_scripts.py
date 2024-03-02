import sqlite3
import json
import os

def create_or_sqlite3_db(sqlite3_db_path: str, collection_name) -> None:
    try:
        conn = sqlite3.connect(sqlite3_db_path)
        cursor = conn.cursor()
        cursor.execute(f'CREATE TABLE IF NOT EXISTS {collection_name} (_id TEXT PRIMARY KEY, value TEXT)')
        conn.commit()
    except Exception as e:
        raise ValueError(f'Failed to create or open kv store db: {str(e)}')
    


def move_json_to_sqlite3(json_path: str, sqlite3_db_path: str, collection_name: str) -> None:
    try:
        with open(json_path, 'r') as file:
            data = json.load(file)
        conn = sqlite3.connect(sqlite3_db_path)
        cursor = conn.cursor()
        for id, value in data.items():
            cursor.execute(f'INSERT INTO {collection_name} (_id, value) VALUES (?, ?)', (id, json.dumps(value)))
        conn.commit()
    except Exception as e:
        raise e

def retrieve_value_from_sqlite3(sqlite3_db_path: str, collection_name: str, _id: str) -> str:
    try:
        conn = sqlite3.connect(sqlite3_db_path)
        cursor = conn.cursor()
        cursor.execute(f'SELECT value FROM {collection_name} WHERE _id = ?', (_id,))
        value = cursor.fetchone()[0]
        return value
    except Exception as e:
        raise ValueError(f'Failed to retrieve value from SQLite3: {str(e)}')


json_path = 'swarmstar/actions/action_space.json'
sqlite3_db_path = 'swarmstar/internal_metadata.sqlite3'

if os.path.exists(sqlite3_db_path):
    os.remove(sqlite3_db_path)

create_or_sqlite3_db(sqlite3_db_path, 'action_space')
move_json_to_sqlite3(json_path, sqlite3_db_path, 'action_space')
