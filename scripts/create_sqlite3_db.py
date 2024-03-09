import sqlite3
import json

def create_or_open_kv_db(sqlite3_db_path: str, table_name: str) -> None:
    try:
        conn = sqlite3.connect(sqlite3_db_path)
        cursor = conn.cursor()
        cursor.execute(f'CREATE TABLE IF NOT EXISTS {table_name} (_id TEXT PRIMARY KEY, value TEXT)')
        conn.commit()
    except Exception as e:
        raise ValueError(f'Failed to create or open {table_name} in db: {str(e)}')
    


def move_json_to_sqlite3(json_path: str, sqlite3_db_path: str, table_name: str) -> None:
    try:
        with open(json_path, 'r') as file:
            data = json.load(file)
        conn = sqlite3.connect(sqlite3_db_path)
        cursor = conn.cursor()
        for key, value in data.items():
            prefixed_key = key
            cursor.execute(f'INSERT INTO {table_name} (_id, value) VALUES (?, ?)', (prefixed_key, json.dumps(value)))
        conn.commit()
    except Exception as e:
        raise e


json_path = 'swarmstar/actions/action_space.json'
sqlite3_db_path = 'swarmstar/internal_metadata.sqlite3'
create_or_open_kv_db(sqlite3_db_path, "action_space")
move_json_to_sqlite3(json_path, sqlite3_db_path, "action_space")

# x = retrieve_value_from_sqlite3(sqlite3_db_path, 'action_space_swarmstar/actions/reasoning')

# print(x)
# print(type(x))
# # Turn json string to dict
# x = json.loads(x)

# print(x)
# print(type(x))

# path = '/Users/brianprzezdziecki/Code/autonomous-general-agent-swarm/swarmstar/actions/action_space_metadata.sqlite3'
# create_or_open_kv_db(path)

