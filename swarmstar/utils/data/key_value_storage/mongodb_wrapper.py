from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError
from pymongo import ReturnDocument
from dotenv import load_dotenv
import os
from bson.binary import Binary

from swarmstar.utils.data.key_value_storage.abstract import KV_Database

load_dotenv()
MONGODB_URI = os.getenv("MONGODB_URI")
MONGODB_DB_NAME = os.getenv("SWARMSTAR_PACKAGE_MONGODB_DB_NAME")

class MongoDBWrapper(KV_Database):
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if not hasattr(self, 'client'):
            self.client = MongoClient(MONGODB_URI)
        self.db = self.client[MONGODB_DB_NAME]

    def insert(self, category, key, value):
        try:
            collection = self.db[category]
            value.pop("id", None)  # Remove the _id field if it exists
            value.pop("_id", None)  # Remove the _id field if it exists
            document = {"_id": key, "version": 1, **value}
            collection.insert_one(document)
        except DuplicateKeyError:
            raise ValueError(f"A document with _id {key} already exists in collection {category}.")

    def replace(self, category, key, value):
        try:
            collection = self.db[category]
            value.pop("id", None)  # Remove the _id field if it exists
            value.pop("_id", None)  # Remove the _id field if it exists

            retries = 5
            for attempt in range(retries):
                current_document = collection.find_one({"_id": key})
                if current_document is None:
                    raise ValueError(f"_id {key} not found in the collection {category}.")

                new_version = current_document.get("version", 0) + 1
                new_document = value.copy()
                new_document["version"] = new_version

                result = collection.replace_one(
                    {"_id": key, "version": current_document["version"]}, new_document
                )

                if result.matched_count:
                    break
                elif attempt == retries - 1:
                    raise Exception("Failed to set value due to concurrent modification.")
        except Exception as e:
            raise ValueError(f"Failed to set value: {str(e)}")

    def update(self, category, key, updated_values):
        try:
            collection = self.db[category]
            updated_values.pop("id", None)  # Remove the _id field if it exists

            retries = 3
            for attempt in range(retries):
                current_document = collection.find_one({"_id": key})
                if current_document is None:
                    raise ValueError(f"_id {key} not found in the collection {category}.")

                new_version = current_document.get("version", 0) + 1
                update_fields = {"version": new_version}
                for field, value in updated_values.items():
                    if field not in current_document:
                        raise KeyError(f"Field '{field}' does not exist in the document {key} in collection {category}.")
                    update_fields[field] = value

                result = collection.update_one(
                    {"_id": key, "version": current_document["version"]},
                    {"$set": update_fields},
                )

                if result.matched_count:
                    break
                elif attempt == retries - 1:
                    raise Exception("Failed to update document due to concurrent modification.")
        except Exception as e:
            raise ValueError(f"Failed to update document: {str(e)}")

    def get(self, category, key):
        collection = self.db[category]
        result = collection.find_one({"_id": key})
        if result is None:
            raise ValueError(f"_id {key} not found in the collection {category}.")
        result.pop("_id")
        result["id"] = key
        return result

    def delete(self, category, key):
        collection = self.db[category]
        result = collection.delete_one({"_id": key})
        if result.deleted_count == 0:
            raise ValueError(f"_id {key} not found in the collection {category}.")

    def exists(self, category, key):
        collection = self.db[category]
        return collection.count_documents({"_id": key}) > 0

    def append_to_list(self, category, key, inner_key, value):
        """
        Append a value to a list stored under a specified key. If the key does not exist, create a new list with the value.

        :param category: Collection name.
        :param key: Document key.
        :param inner_key: Inner key of the list to append the value to.
        :param value: Value to append to the list.
        """
        collection = self.db[category]
        try:
            existing_document = collection.find_one({"_id": key})
            if existing_document:
                if type(existing_document[inner_key]) != list:
                    raise ValueError(f"_id {key} exists in the collection {category} but is not a list.")
                collection.find_one_and_update(
                    {"_id": key},
                    {"$push": {inner_key: value}},
                    return_document=ReturnDocument.AFTER
                )
            else:
                document = {"_id": key, inner_key: [value]}
                collection.insert_one(document)
        except Exception as e:
            raise ValueError(f"Failed to append to list: {str(e)}")

    def remove_from_list(self, category, key, inner_key, value):
        """
        Remove a value from a list stored under a specified key.
        
        :param category: Collection name.
        :param key: Document key.
        :param inner_key: Inner key of the list to remove the value from.
        :param value: Value to remove from the list.
        """
        collection = self.db[category]
        collection.find_one_and_update(
            {"_id": key},
            {"$pull": {inner_key: value}},
            return_document=ReturnDocument.AFTER
        )
