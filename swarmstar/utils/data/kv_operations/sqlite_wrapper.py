import sqlite3

from swarmstar.utils.data.kv_operations.kv_database import KV_Database

class SQLiteWrapper(KV_Database):
    _instance = None

    def __new__(cls, db_name):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, db_name):
        if not hasattr(self, 'conn'):
            self.conn = sqlite3.connect(db_name)
            self.create_tables()

    def create_tables(self):
        cursor = self.conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS kv_store (
                category TEXT,
                key TEXT,
                value TEXT,
                version INTEGER,
                PRIMARY KEY (category, key)
            )
        """)
        self.conn.commit()

    def insert(self, category, key, value):
        try:
            cursor = self.conn.cursor()
            cursor.execute("""
                INSERT INTO kv_store (category, key, value, version)
                VALUES (?, ?, ?, ?)
            """, (category, key, str(value), 1))
            self.conn.commit()
        except sqlite3.IntegrityError:
            raise ValueError(f"A document with key {key} already exists in category {category}.")

    def set(self, category, key, value):
        try:
            cursor = self.conn.cursor()
            cursor.execute("""
                UPDATE kv_store
                SET value = ?, version = version + 1
                WHERE category = ? AND key = ?
            """, (str(value), category, key))
            if cursor.rowcount == 0:
                raise ValueError(f"Key {key} not found in category {category}.")
            self.conn.commit()
        except Exception as e:
            raise ValueError(f"Failed to set value: {str(e)}")

    def update(self, category, key, updated_values):
        try:
            cursor = self.conn.cursor()
            current_value = self.get(category, key)
            for field, value in updated_values.items():
                if field not in current_value:
                    raise KeyError(f"Field '{field}' does not exist in the document.")
                current_value[field] = value
            cursor.execute("""
                UPDATE kv_store
                SET value = ?, version = version + 1
                WHERE category = ? AND key = ?
            """, (str(current_value), category, key))
            self.conn.commit()
        except Exception as e:
            raise ValueError(f"Failed to update document: {str(e)}")

    def get(self, category, key):
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT value FROM kv_store
            WHERE category = ? AND key = ?
        """, (category, key))
        result = cursor.fetchone()
        if result is None:
            raise ValueError(f"Key {key} not found in category {category}.")
        return eval(result[0])

    def delete(self, category, key):
        cursor = self.conn.cursor()
        cursor.execute("""
            DELETE FROM kv_store
            WHERE category = ? AND key = ?
        """, (category, key))
        if cursor.rowcount == 0:
            raise ValueError(f"Key {key} not found in category {category}.")
        self.conn.commit()

    def exists(self, category, key):
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT COUNT(*) FROM kv_store
            WHERE category = ? AND key = ?
        """, (category, key))
        count = cursor.fetchone()[0]
        return count > 0

    def append(self, category, key, value):
        try:
            current_value = self.get(category, key)
            if isinstance(current_value, list):
                current_value.append(value)
            else:
                current_value = [current_value, value]
            self.set(category, key, current_value)
        except ValueError:
            self.insert(category, key, [value])

    def remove_from_list(self, category, key, value):
        try:
            current_value = self.get(category, key)
            if isinstance(current_value, list):
                current_value.remove(value)
                self.set(category, key, current_value)
            else:
                raise ValueError(f"Value associated with key {key} in category {category} is not a list.")
        except ValueError as e:
            raise ValueError(f"Failed to remove value from list: {str(e)}")