import sqlite3
import json

def create_or_open_kv_db(sqlite3_db_path: str) -> None:
    try:
        conn = sqlite3.connect(sqlite3_db_path)
        cursor = conn.cursor()
        cursor.execute('CREATE TABLE IF NOT EXISTS kv_store (key TEXT PRIMARY KEY, value TEXT)')
        conn.commit()
    except Exception as e:
        raise ValueError(f'Failed to create or open kv store db: {str(e)}')
    


def move_json_to_sqlite3(json_path: str, sqlite3_db_path: str) -> None:
    try:
        with open(json_path, 'r') as file:
            data = json.load(file)
        conn = sqlite3.connect(sqlite3_db_path)
        cursor = conn.cursor()
        for key, value in data.items():
            # Prefixing each key with "action_space"
            prefixed_key = f"action_space_{key}"
            cursor.execute('INSERT INTO kv_store (key, value) VALUES (?, ?)', (prefixed_key, json.dumps(value)))
        conn.commit()
    except Exception as e:
        raise ValueError(f'Failed to move JSON to SQLite3: {str(e)}')

def retrieve_value_from_sqlite3(sqlite3_db_path: str, key: str) -> str:
    try:
        conn = sqlite3.connect(sqlite3_db_path)
        cursor = conn.cursor()
        cursor.execute('SELECT value FROM kv_store WHERE key = ?', (key,))
        value = cursor.fetchone()[0]
        return value
    except Exception as e:
        raise ValueError(f'Failed to retrieve value from SQLite3: {str(e)}')


json_path = 'aga_swarm/actions/action_space_metadata.json'
sqlite3_db_path = 'aga_swarm/actions/action_space_metadata.sqlite3'
# move_json_to_sqlite3(json_path, sqlite3_db_path)

x = retrieve_value_from_sqlite3(sqlite3_db_path, 'action_space_aga_swarm/actions/reasoning')

print(x)
print(type(x))
# Turn json string to dict
x = json.loads(x)

print(x)
print(type(x))

# path = '/Users/brianprzezdziecki/Code/autonomous-general-agent-swarm/aga_swarm/actions/action_space_metadata.sqlite3'
# create_or_open_kv_db(path)

