from __future__ import annotations

import subprocess
from importlib import resources
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


def restore_database(package_name: str, resource_name: str, uri: str, db_name: str):
    """
    Restore a MongoDB database dump to a specified database from package resources.

    :param package_name: Name of the package containing the dump files.
    :param resource_name: The resource name/path within the package.
    :param uri: MongoDB URI for connecting to the target instance.
    :param db_name: Name of the database to restore the dump into.
    """
    # Use importlib.resources to resolve the path to the resource
    with resources.path(package_name, resource_name) as dump_path:
        # Construct the mongorestore command
        restore_command = ["mongorestore", "--uri", uri, "--db", db_name, str(dump_path)]

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
    
def add_kv(swarm: SwarmConfig, category: str, key: str, value: dict) -> None:
    """
    Add a key-value pair to the collection with an initial version number.
    """
    try:
        db_name = swarm.mongodb_db_name
        collection_name = category
        uri = swarm.mongodb_uri
        client = create_client(uri)
        db = client[db_name]
        if collection_name not in db.list_collection_names():
            create_collection(swarm, collection_name)
        collection = db[collection_name]
        # Initialize the document with a version number
        document = {"key": key, "version": 1, **value}
        collection.insert_one(document)
    except pymongo.errors.DuplicateKeyError:
        update_kv(swarm, category, key, value)
    except Exception as e:
        raise ValueError(f'Failed to add to MongoDB collection: {str(e)}')


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
        result.pop("version")
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

def update_kv(swarm: SwarmConfig, category: str, key: str, updated_values: dict) -> None:
    """
    Update specified fields of a document and increment its version, ensuring optimistic concurrency control.
    """
    try:
        uri = swarm.mongodb_uri
        db_name = swarm.mongodb_db_name
        collection_name = category
        client = create_client(uri)
        db = client[db_name]
        collection = db[collection_name]
        
        retries = 3
        for attempt in range(retries):
            # Fetch the current document
            current_document = collection.find_one({"key": key})
            if current_document is None:
                raise ValueError(f'Key {key} not found in MongoDB collection {collection_name}.')

            # Prepare the update
            new_version = current_document.get("version", 0) + 1
            update_fields = {"version": new_version}
            for field, value in updated_values.items():
                if field not in current_document:
                    raise KeyError(f"Field '{field}' does not exist in the document.")
                update_fields[field] = value

            # Attempt to update the document if the version hasn't changed
            result = collection.update_one(
                {"key": key, "version": current_document["version"]},
                {"$set": update_fields}
            )

            if result.matched_count:
                break  # Update was successful
            elif attempt == retries - 1:
                raise Exception("Failed to update document due to concurrent modification.")
            # If the document was updated elsewhere, retry the operation
    except Exception as e:
        raise ValueError(f"Failed to update MongoDB collection: {str(e)}")

def append_to_list_with_versioning(swarm: SwarmConfig, category: str, key: str, list_field: str, value_to_append) -> None:
    """
    Appends a value to a list within a document, using optimistic concurrency control to handle concurrent updates safely.

    :param collection_name: The name of the collection.
    :param key: The key identifying the document.
    :param list_field: The field within the document that contains the list to append to.
    :param value_to_append: The value to append to the list.
    """
    try:
        uri = swarm.mongodb_uri
        db_name = swarm.mongodb_db_name
        collection_name = category
        client = create_client(uri)
        db = client[db_name]
        collection = db[collection_name]

        retries = 3
        for attempt in range(retries):
            # Fetch the current document
            current_document = collection.find_one({"key": key})
            if current_document is None:
                raise ValueError(f'Key {key} not found in MongoDB collection {collection_name}.')
            if list_field not in current_document:
                raise KeyError(f"Field '{list_field}' does not exist in the document. Ensure the field is initialized as a list.")

            # Prepare the update with an incremented version number
            new_version = current_document.get("version", 0) + 1
            updated_values = {"$push": {list_field: value_to_append}, "$set": {"version": new_version}}

            # Attempt to update the document if the version hasn't changed
            result = collection.update_one(
                {"key": key, "version": current_document["version"]},
                updated_values
            )

            if result.matched_count:
                break  # Update was successful
            elif attempt == retries - 1:
                raise Exception("Failed to update document due to concurrent modification.")
            # If the document was updated elsewhere, retry the operation
    except Exception as e:
        raise ValueError(f"Failed to append to list in MongoDB collection: {str(e)}")

def add_to_dict_with_versioning(swarm: SwarmConfig, category: str, key: str, dict_field: str, dict_key: str, dict_value) -> None:
    """
    Adds a key-value pair to a dictionary within a document, using optimistic concurrency control to handle concurrent updates safely.

    :param collection_name: The name of the collection.
    :param key: The key identifying the document.
    :param dict_field: The field within the document that contains the dictionary to add to.
    :param dict_key: The key to add to the dictionary.
    :param dict_value: The value to associate with the dict_key in the dictionary.
    """
    try:
        uri = swarm.mongodb_uri
        db_name = swarm.mongodb_db_name
        collection_name = category
        client = create_client(uri)
        db = client[db_name]
        collection = db[collection_name]

        retries = 3
        for attempt in range(retries):
            # Fetch the current document
            current_document = collection.find_one({"key": key})
            if current_document is None:
                raise ValueError(f'Key {key} not found in MongoDB collection {collection_name}.')
            if dict_field not in current_document:
                raise KeyError(f"Field '{dict_field}' does not exist in the document. Ensure the field is initialized as a dictionary.")

            # Prepare the update with an incremented version number
            new_version = current_document.get("version", 0) + 1
            updated_values = {
                "$set": {
                    f"{dict_field}.{dict_key}": dict_value,  # This adds or updates the key in the dictionary
                    "version": new_version
                }
            }

            # Attempt to update the document if the version hasn't changed
            result = collection.update_one(
                {"key": key, "version": current_document["version"]},
                updated_values
            )

            if result.matched_count:
                break  # Update was successful
            elif attempt == retries - 1:
                raise Exception("Failed to update document due to concurrent modification.")
            # If the document was updated elsewhere, retry the operation
    except Exception as e:
        raise ValueError(f"Failed to add to dictionary in MongoDB collection: {str(e)}")