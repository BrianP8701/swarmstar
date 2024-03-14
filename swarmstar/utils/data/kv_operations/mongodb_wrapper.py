from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError
from dotenv import load_dotenv
import os

from swarmstar.utils.data.kv_operations.kv_database import KV_Database

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
            value.pop("_id", None)  # Remove the _id field if it exists
            document = {"_id": key, "version": 1, **value}
            collection.insert_one(document)
        except DuplicateKeyError:
            raise ValueError(f"A document with _id {key} already exists in collection {category}.")

    def set(self, category, key, value):
        try:
            collection = self.db[category]
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
            updated_values.pop("_id", None)  # Remove the _id field if it exists

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

    def append(self, category, key, value):
        collection = self.db[category]
        result = collection.find_one({"_id": key})
        if result:
            if "data" not in result:
                collection.update_one({"_id": key}, {"$set": {"data": []}})
            collection.update_one({"_id": key}, {"$push": {"data": value}})
        else:
            self.insert(category, key, {"data": [value]})

    def remove_from_list(self, category, key, value):
        collection = self.db[category]
        if collection.count_documents({"_id": key}) == 0:
            raise ValueError(f"_id {key} not found in the collection {category}.")

        result = collection.update_one({"_id": key}, {"$pull": {"data": value}})

        if result.modified_count == 0:
            raise ValueError(f"Value {value} not found in the list associated with _id {key}.")
