from __future__ import annotations
from typing import TYPE_CHECKING
from pymongo import MongoClient
import pymongo
import subprocess

if TYPE_CHECKING:
    from aga_swarm.swarm.types import Swarm

def restore_database(dump_path: str, uri: str, db_name: str):
    """
    Restore a MongoDB database dump to a specified database.

    :param dump_path: Path to the directory containing the dump files.
    :param uri: MongoDB URI for connecting to the target instance.
    :param db_name: Name of the database to restore the dump into.
    """
    # Construct the mongorestore command
    restore_command = [
        "mongorestore",
        "--uri", uri,
        "--db", db_name,
        dump_path
    ]

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
        raise ValueError(f'Failed to create MongoDB client: {str(e)}')
    

def create_collection_with_unique_index(swarm: Swarm, collection_name: str) -> None:
    uri = swarm.configs.mongodb_uri
    db_name = swarm.configs.mongodb_db_name
    client = create_client(uri)
    db = client[db_name]
    collection = db[collection_name]
    collection.create_index([('key', pymongo.ASCENDING)], unique=True)
    

def upload_swarm_space_kv_pair(swarm: Swarm, category: str, key: str, value: dict) -> None:
    db_name = swarm.configs.mongodb_db_name
    collection_name = category
    uri = swarm.configs.mongodb_uri
    client = create_client(uri)
    db = client[db_name]
    collection = db[collection_name]
    collection.create_index([('key', pymongo.ASCENDING)], unique=True)


def retrieve_swarm_space_kv_value(swarm: Swarm, category: str, key: str) -> dict:
    try:    
        uri = swarm.configs.mongodb_uri
        db_name = swarm.configs.mongodb_db_name
        collection_name = category
        client = create_client(uri)
        db = client[db_name]
        collection = db[collection_name]
        result = collection.find_one({"key": key})
        if result is None:
            raise ValueError(f'Key {key} not found in MongoDB collection.')
        return result
    except Exception as e:
        raise ValueError(f'Failed to get from MongoDB collection: {str(e)}')

def delete_swarm_space_kv_pair(swarm: Swarm, category: str, key: str) -> None:
    try:
        uri = swarm.configs.mongodb_uri
        db_name = swarm.configs.mongodb_db_name
        collection_name = category
        client = create_client(uri)
        db = client[db_name]
        collection = db[collection_name]
        result = collection.delete_one({"key": key})
        if result.deleted_count == 0:
            raise ValueError(f'Key {key} not found in MongoDB collection.')
    except Exception as e:
        raise ValueError(f'Failed to delete from MongoDB collection: {str(e)}')

def update_swarm_space_kv_pair(swarm: Swarm, category: str, key: str, update_value: dict) -> None:
    try:
        uri = swarm.configs.mongodb_uri
        db_name = swarm.configs.mongodb_db_name
        collection_name = category
        client = create_client(uri)
        db = client[db_name]
        collection = db[collection_name]
        result = collection.update_one({"key": key}, {"$set": update_value})
        if result.matched_count == 0:
            raise ValueError(f'Key {key} not found in MongoDB collection.')
    except Exception as e:
        raise ValueError(f'Failed to update MongoDB collection: {str(e)}')
