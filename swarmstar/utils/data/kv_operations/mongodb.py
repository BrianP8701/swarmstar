from __future__ import annotations

import subprocess
from typing import TYPE_CHECKING

import pymongo
from pymongo import MongoClient

if TYPE_CHECKING:
    from swarmstar.swarm.types import SwarmConfig


def check_and_create_database(mongodb_uri: str, db_name: str) -> None:
    """
    Check if a MongoDB database exists, and if not, create it.

    :param mongodb_uri: MongoDB URI for connecting to the instance.
    :param db_name: Name of the database to check and potentially create.
    :raises ValueError: If the database already exists.
    """
    client = MongoClient(mongodb_uri)
    if db_name in client.list_database_names():
        raise ValueError(f"Database {db_name} already exists.")
    else:
        db = client[db_name]
        collection = db["stage"]
        collection.insert_one({"_id": "dummy_id"})
        collection.delete_one({"_id": "dummy_id"})
        print(f"Database {db_name} created successfully.")


def restore_database(dump_path: str, uri: str, db_name: str):
    """
    Restore a MongoDB database dump to a specified database.

    :param dump_path: Path to the directory containing the dump files.
    :param uri: MongoDB URI for connecting to the target instance.
    :param db_name: Name of the database to restore the dump into.
    """
    # Construct the mongorestore command
    restore_command = ["mongorestore", "--uri", uri, "--db", db_name, dump_path]

    try:
        # Execute the mongorestore command
        subprocess.run(restore_command, check=True)
        print("Database restored successfully.")
    except subprocess.CalledProcessError as e:
        raise ValueError(f"Failed to restore database: {e}")


def create_client(uri: str) -> MongoClient:
    try:
        client = MongoClient(uri)
        return client
    except Exception as e:
        raise ValueError(f"Failed to create MongoDB client: {str(e)}")


def create_collection(swarm: SwarmConfig, category: str) -> None:
    uri = swarm.mongodb_uri
    db_name = swarm.mongodb_db_name
    client = create_client(uri)
    db = client[db_name]
    collection = db[category]
    collection.create_index([("key", pymongo.ASCENDING)], unique=True)


def add_kv(swarm: SwarmConfig, category: str, key: str, value: dict) -> None:
    try:
        db_name = swarm.mongodb_db_name
        collection_name = category
        uri = swarm.mongodb_uri
        client = create_client(uri)
        db = client[db_name]
        if collection_name not in db.list_collection_names():
            create_collection(swarm, collection_name)
        collection = db[collection_name]
        document = {"key": key, **value}
        collection.insert_one(document)
    except pymongo.errors.DuplicateKeyError as e:
        update_kv(swarm, category, key, value)
    except Exception as e:
        raise ValueError(f"Failed to add to MongoDB collection: {str(e)}")


def get_kv(swarm: SwarmConfig, category: str, key: str) -> dict:
    try:
        uri = swarm.mongodb_uri
        db_name = swarm.mongodb_db_name
        collection_name = category
        client = create_client(uri)
        db = client[db_name]
        if collection_name not in db.list_collection_names():
            create_collection(swarm, collection_name)
        collection = db[collection_name]
        result = collection.find_one({"key": key})
        if result is None:
            raise ValueError(f"Key {key} not found in MongoDB collection.")
        result.pop("_id")
        result.pop("key")
        return result
    except Exception as e:
        raise ValueError(f"Failed to get from MongoDB collection: {str(e)}")


def delete_kv(swarm: SwarmConfig, category: str, key: str) -> None:
    try:
        uri = swarm.mongodb_uri
        db_name = swarm.mongodb_db_name
        collection_name = category
        client = create_client(uri)
        db = client[db_name]
        if collection_name not in db.list_collection_names():
            create_collection(swarm, collection_name)
        collection = db[collection_name]
        result = collection.delete_one({"key": key})
        if result.deleted_count == 0:
            raise ValueError(f"Key {key} not found in MongoDB collection.")
    except Exception as e:
        raise ValueError(f"Failed to delete from MongoDB collection: {str(e)}")


def update_kv(swarm: SwarmConfig, category: str, key: str, value: dict) -> None:
    try:
        uri = swarm.mongodb_uri
        db_name = swarm.mongodb_db_name
        collection_name = category
        client = create_client(uri)
        db = client[db_name]
        collection = db[collection_name]
        if collection_name not in db.list_collection_names():
            create_collection(swarm, collection_name)
        result = collection.update_one({"key": key}, {"$set": value})
        if result.matched_count == 0:
            raise ValueError(f"Key {key} not found in MongoDB collection.")
    except Exception as e:
        raise ValueError(f"Failed to update MongoDB collection: {str(e)}")
