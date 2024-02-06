import sqlite3

def create_or_open_kv_db(sqlite3_db_path: str) -> None:
    try:
        conn = sqlite3.connect(sqlite3_db_path)
        cursor = conn.cursor()
        cursor.execute('CREATE TABLE IF NOT EXISTS kv_store (key TEXT PRIMARY KEY, value TEXT)')
        conn.commit()
    except Exception as e:
        raise ValueError(f'Failed to create or open kv store db: {str(e)}')
    

    
path = '/Users/brianprzezdziecki/Code/autonomous-general-agent-swarm/aga_swarm/actions/action_space_metadata.db'
create_or_open_kv_db(path)