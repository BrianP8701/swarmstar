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
        collection = db["swarm"]
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

def add_kv(swarm: SwarmConfig, collection: str, _id: str, value: dict) -> None:
    """
    Add a _id-value pair to the collection with an initial version number.
    """
    try:
        db_name = swarm.mongodb_db_name
        collection_name = collection
        uri = swarm.mongodb_uri
        client = create_client(uri)
        db = client[db_name]
        collection = db[collection_name]
        value.pop("id", None)
        # Initialize the document with a version number
        document = {"_id": _id, "version": 1, **value}
        collection.insert_one(document)
    except pymongo.errors.DuplicateKeyError:
        update_kv(swarm, collection_name, _id, value)
    except Exception as e:
        raise ValueError(f'Failed to add to MongoDB collection: {str(e)}')


def get_kv(swarm: SwarmConfig, collection: str, _id: str) -> dict:
    try:
        uri = swarm.mongodb_uri
        db_name = swarm.mongodb_db_name
        collection_name = collection
        client = create_client(uri)
        db = client[db_name]
        if collection_name not in db.list_collection_names():
            raise ValueError(f"Collection {collection_name} not found in MongoDB database.")
        collection = db[collection_name]
        result = collection.find_one({"_id": _id})
        if result is None:
            raise ValueError(f"_id {_id} not found in MongoDB collection.")
        return result
    except Exception as e:
        raise ValueError(f"Failed to get from MongoDB collection: {str(e)}")


def delete_kv(swarm: SwarmConfig, collection: str, _id: str) -> None:
    try:
        uri = swarm.mongodb_uri
        db_name = swarm.mongodb_db_name
        collection_name = collection
        client = create_client(uri)
        db = client[db_name]
        if collection_name not in db.list_collection_names():
            raise ValueError(f"Collection {collection_name} not found in MongoDB database.")
        collection = db[collection_name]
        result = collection.delete_one({"_id": _id})
        if result.deleted_count == 0:
            raise ValueError(f"_id {_id} not found in MongoDB collection.")
    except Exception as e:
        raise ValueError(f"Failed to delete from MongoDB collection: {str(e)}")

def update_kv(swarm: SwarmConfig, collection: str, _id: str, updated_values: dict) -> None:
    """
    Update specified fields of a document and increment its version, ensuring optimistic concurrency control.
    """
    try:
        uri = swarm.mongodb_uri
        db_name = swarm.mongodb_db_name
        collection_name = collection
        client = create_client(uri)
        db = client[db_name]
        collection = db[collection_name]
        
        retries = 3
        for attempt in range(retries):
            # Fetch the current document
            current_document = collection.find_one({"_id": _id})
            if current_document is None:
                raise ValueError(f'_id {_id} not found in MongoDB collection {collection_name}.')

            # Prepare the update
            new_version = current_document.get("version", 0) + 1
            update_fields = {"version": new_version}
            for field, value in updated_values.items():
                if field not in current_document:
                    raise KeyError(f"Field '{field}' does not exist in the document.")
                update_fields[field] = value

            # Attempt to update the document if the version hasn't changed
            result = collection.update_one(
                {"_id": _id, "version": current_document["version"]},
                {"$set": update_fields}
            )

            if result.matched_count:
                break  # Update was successful
            elif attempt == retries - 1:
                raise Exception("Failed to update document due to concurrent modification.")
            # If the document was updated elsewhere, retry the operation
    except Exception as e:
        raise ValueError(f"Failed to update MongoDB collection: {str(e)}")

def set_kv(swarm: SwarmConfig, collection: str, _id: str, new_value: dict) -> None:
    """
    Replace the value of a document with the new value provided, ensuring optimistic concurrency control.
    """
    try:
        uri = swarm.mongodb_uri
        db_name = swarm.mongodb_db_name
        collection_name = collection
        client = create_client(uri)  # Assume create_client is defined elsewhere
        db = client[db_name]
        collection = db[collection_name]

        retries = 5
        for attempt in range(retries):
            # Fetch the current document
            current_document = collection.find_one({"_id": _id})
            if current_document is None:
                raise ValueError(f'_id {_id} not found in MongoDB collection {collection_name}.')

            # Prepare the new document with incremented version
            new_version = current_document.get("version", 0) + 1
            new_document = new_value.copy()  # Make a copy to avoid mutating the original argument
            new_document["version"] = new_version

            # Attempt to replace the document if the version hasn't changed
            result = collection.replace_one(
                {"_id": _id, "version": current_document["version"]},
                new_document
            )

            if result.matched_count:
                break  # Update was successful
            elif attempt == retries - 1:
                raise Exception("Failed to replace document due to concurrent modification.")
            # If the document was updated elsewhere, retry the operation
    except Exception as e:
        raise ValueError(f"Failed to replace document in MongoDB collection: {str(e)}")

# def append_to_list(swarm: SwarmConfig, collection: str, _id: str, value) -> None:
#     """
#     Append a value to a list within a document identified by _id without reading the whole list.
#     """
#     try:
#         uri = swarm.mongodb_uri
#         db_name = swarm.mongodb_db_name
#         client = create_client(uri)
#         db = client[db_name]
#         collection = db[collection]
        
#         collection.update_one({"_id": _id}, {"$push": {"listFieldName": value}})
#         print("Value appended successfully.")
#     except Exception as e:
#         raise ValueError(f"Failed to append value to list in MongoDB collection: {str(e)}")

# def get_element_by_index(swarm: SwarmConfig, collection: str, _id: str, index: int) -> any:
#     """
#     Retrieve an element by index from a list within a document without retrieving the whole list.
#     """
#     try:
#         uri = swarm.mongodb_uri
#         db_name = swarm.mongodb_db_name
#         client = create_client(uri)
#         db = client[db_name]
#         collection = db[collection]
        
#         result = collection.find_one({"_id": _id}, {"listFieldName": {"$slice": [index, 1]}})
#         if result and "listFieldName" in result and len(result["listFieldName"]) > 0:
#             return result["listFieldName"][0]
#         else:
#             raise ValueError("Element at specified index not found.")
#     except Exception as e:
#         raise ValueError(f"Failed to retrieve element by index: {str(e)}")

# def get_list_length(swarm: SwarmConfig, collection: str, _id: str) -> int:
#     """
#     Get the length of a list within a document without retrieving the list itself.
#     """
#     try:
#         uri = swarm.mongodb_uri
#         db_name = swarm.mongodb_db_name
#         client = create_client(uri)
#         db = client[db_name]
#         collection = db[collection]
        
#         pipeline = [
#             {"$match": {"_id": _id}},
#             {"$project": {"length": {"$size": "$listFieldName"}}}
#         ]
#         result = list(collection.aggregate(pipeline))
#         if result and len(result) > 0:
#             return result[0]["length"]
#         else:
#             raise ValueError("_id not found or list is empty.")
#     except Exception as e:
#         raise ValueError(f"Failed to get list length: {str(e)}")
