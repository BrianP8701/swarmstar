import subprocess
from importlib import resources

import pymongo
from pymongo import MongoClient


def check_and_create_mongodb_database(mongodb_uri: str, db_name: str) -> None:
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
        collection = db["config"]
        collection.insert_one({"_id": "dummy_id"})
        collection.delete_one({"_id": "dummy_id"})
        print(f"Database {db_name} created successfully.")


def restore_mongodb_database(package_name: str, resource_name: str, uri: str, db_name: str):
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


def create_mongodb_client(uri: str) -> MongoClient:
    try:
        client = MongoClient(uri)
        return client
    except Exception as e:
        raise ValueError(f"Failed to create MongoDB client: {str(e)}")

def mongodb_add_kv(mongodb_uri: str, mongodb_db_name: str, collection_name: str, _id: str, value: dict) -> None:
    """
    Add a _id-value pair to the collection with an initial version number.
    """
    try:
        uri = mongodb_uri
        db_name = mongodb_db_name
        client = create_mongodb_client(uri)
        db = client[db_name]
        collection = db[collection_name]
        value.pop("id", None)
        # Initialize the document with a version number
        document = {"_id": _id, "version": 1, **value}
        collection.insert_one(document)
    except pymongo.errors.DuplicateKeyError:
        mongodb_set_kv(mongodb_uri, mongodb_db_name, collection_name, _id, value)
    except Exception as e:
        raise ValueError(f'Failed to add to MongoDB collection: {str(e)}')


def mongodb_get_kv(mongodb_uri: str, mongodb_db_name: str, collection_name: str, _id: str) -> dict:
    """
    Retrieve a document by _id from the collection.
    """
    try:
        uri = mongodb_uri
        db_name = mongodb_db_name
        client = create_mongodb_client(uri)
        db = client[db_name]
        if collection_name not in db.list_collection_names():
            raise ValueError(f"Collection {collection_name} not found in MongoDB database.")
        collection = db[collection_name]
        result = collection.find_one({"_id": _id})
        if result is None:
            raise ValueError(f"_id {_id} not found in MongoDB collection {collection_name}.")
        id = result.pop("_id")
        result["id"] = id
        return result
    except Exception as e:
        raise ValueError(f"Failed to get from MongoDB collection: {str(e)}")


def mongodb_delete_kv(mongodb_uri: str, mongodb_db_name: str, collection_name: str, _id: str) -> None:
    try:
        uri = mongodb_uri
        db_name = mongodb_db_name
        client = create_mongodb_client(uri)
        db = client[db_name]
        if collection_name not in db.list_collection_names():
            raise ValueError(f"Collection {collection_name} not found in MongoDB database.")
        collection = db[collection_name]
        result = collection.delete_one({"_id": _id})
        if result.deleted_count == 0:
            raise ValueError(f"_id {_id} not found in MongoDB collection {collection_name}.")
    except Exception as e:
        raise ValueError(f"Failed to delete from MongoDB collection: {str(e)}")

def mongodb_update_kv(mongodb_uri: str, mongodb_db_name: str, collection_name: str, _id: str, updated_values: dict) -> None:
    """
    Update specified fields of a document and increment its version, ensuring optimistic concurrency control.
    """
    try:
        uri = mongodb_uri
        db_name = mongodb_db_name
        client = create_mongodb_client(uri)
        db = client[db_name]
        collection = db[collection_name]
        updated_values.pop("id", None)

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

def mongodb_set_kv(mongodb_uri: str, mongodb_db_name: str, collection_name: str, _id: str, new_value: dict) -> None:
    """
    Replace the value of a document with the new value provided, ensuring optimistic concurrency control.
    """
    try:
        uri = mongodb_uri
        db_name = mongodb_db_name
        client = create_mongodb_client(uri)
        db = client[db_name]
        collection = db[collection_name]
        new_value.pop("id", None)

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

def mongodb_append_to_list(mongodb_uri: str, mongodb_db_name: str, collection_name: str, _id: str, key: str, value) -> None:
    """
    Append a value to a list within a document identified by _id, creating the document or list if they do not exist.
    """
    try:
        uri = mongodb_uri
        db_name = mongodb_db_name
        client = create_mongodb_client(uri)
        db = client[db_name]
        collection = db[collection_name]
        
        if collection.count_documents({"_id": _id}) > 0:
            collection.update_one({"_id": _id}, {"$push": {key: value}}, upsert=True)
        else:
            mongodb_add_kv(mongodb_uri, mongodb_db_name, collection_name, _id, {key: [value]})
            
    except Exception as e:
        raise ValueError(f"Failed to append value {value} to list in MongoDB collection {collection_name}: {str(e)}")


def mongodb_get_element_by_index(mongodb_uri: str, mongodb_db_name: str, collection_name: str, _id: str, index: int) -> any:
    """
    Retrieve an element by index from a list within a document without retrieving the whole list.
    """
    try:
        uri = mongodb_uri
        db_name = mongodb_db_name
        client = create_mongodb_client(uri)
        db = client[db_name]
        collection = db[collection_name]
        
        result = collection.find_one({"_id": _id}, {"data": {"$slice": [index, 1]}})
        if result and "data" in result and len(result["data"]) > 0:
            return result["data"][0]
        else:
            raise ValueError(f"Element at index {index} not found in list in MongoDB collection {collection_name}.")
    except Exception as e:
        raise ValueError(f"Failed to retrieve element by index: {str(e)}")

def mongodb_get_list_length(mongodb_uri: str, mongodb_db_name: str, collection_name: str, _id: str) -> int:
    """
    Get the length of a list within a document without retrieving the list itself.
    """
    try:
        uri = mongodb_uri
        db_name = mongodb_db_name
        client = create_mongodb_client(uri)
        db = client[db_name]
        collection = db[collection_name]
        
        pipeline = [
            {"$match": {"_id": _id}},
            {"$project": {"length": {"$size": "$data"}}}
        ]
        result = list(collection.aggregate(pipeline))
        if result and len(result) > 0:
            return result[0]["length"]
        else:
            raise ValueError(f"_id {_id} not found or list is empty in MongoDB collection {collection_name}.")
    except Exception as e:
        raise ValueError(f"Failed to get list length: {str(e)}")
