from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError
from pymongo import ReturnDocument
from pymongo.client_session import ClientSession
import pymongo
from dotenv import load_dotenv
import os
from typing import Dict, Any, List

from swarmstar.utils.database.abstract_database import Database

load_dotenv()
MONGODB_URI = os.getenv("MONGODB_URI")
MONGODB_DB_NAME = os.getenv("SWARMSTAR_PACKAGE_MONGODB_DB_NAME")

class MongoDBWrapper(Database):
    """
    This is a singleton class that wraps the MongoDB client. It's a subclass of the 
    abstract database class, which won't change. However, we'll change this concrete class
    to adapt to scale and performance requirements.
    
    A couple of notes:
        I use pydantic models ALOT. But pydantic models don't allow for fields starting with _.
        MongoDB strictly uses _id as the primary key. So that's why you see me doing a lot of pop("_id", None) in the code.
        On the application and package side we use id, and only in the data layer do we use _id.

        I also use the _version field to handle optimistic concurrency control. This is a simple way to handle
        concurrent updates to the same document.
    """
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if not hasattr(self, 'client'):
            self.client = MongoClient(MONGODB_URI)
        self.db = self.client[MONGODB_DB_NAME]


    """                      CRUD operations                         """
    def create(self, category: str, key: str, value: Dict[str, Any]) -> None:
        try:
            collection = self.db[category]
            value.pop("id", None) 
            document = {"_id": key, "version": 1, **value}
            collection.insert_one(document)
        except DuplicateKeyError:
            raise ValueError(f"A document with _id {key} already exists in collection {category}.")
        except Exception as e:
            raise ValueError(f"Failed to create document: {str(e)}")

    def read(self, category: str, key: str) -> Dict[str, Any]:
        collection = self.db[category]
        result = collection.find_one({"_id": key})
        if result is None:
            raise ValueError(f"_id {key} not found in the collection {category}.")
        result.pop("_id")
        result.pop("version")
        result["id"] = key
        return result

    def update(self, category: str, key: str, updated_fields: Dict[str, Any]) -> None:
        """
        Update a document in the database. If the document does not exist, raise a ValueError.
        Uses optimistic concurrency control to prevent concurrent updates.
        If a field in updated_fields is not present in the document, it will be added.
        """
        try:
            collection = self.db[category]
            updated_fields.pop("id", None)  # Remove the _id field if it exists

            retries = 5
            for attempt in range(retries):
                current_document = collection.find_one({"_id": key})
                if current_document is None:
                    raise ValueError(f"_id {key} not found in the collection {category}.")

                new_version = current_document.get("version", 0) + 1
                update_fields = {"version": new_version}
                for field, value in updated_fields.items():
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
            raise ValueError(f"Failed to update document at {category}/{key}: {str(e)}")

    def delete(self, category, key):
        collection = self.db[category]
        result = collection.delete_one({"_id": key})
        if result.deleted_count == 0:
            raise ValueError(f"_id {key} not found in the collection {category}.")
    
    
    
    """              Managing transaction sessions for atomicity              """
    def begin_transaction(self) -> ClientSession:
        session = self.client.start_session()
        session.start_transaction()
        return session

    def commit_transaction(self, session: ClientSession):
        session.commit_transaction()

    def rollback_transaction(self, session: ClientSession):
        session.abort_transaction()



    """                     Locks                     """
    def lock(self, category: str, key: str) -> bool:
        collection = self.db[category]
        result = collection.update_one(
            {"_id": key, "lock": {"$exists": False}},
            {"$set": {"lock": True}},
            upsert=False
        )
        return result.modified_count > 0

    def unlock(self, category: str, key: str) -> None:
        collection = self.db[category]
        collection.update_one(
            {"_id": key},
            {"$unset": {"lock": ""}}
        )




    """                     Other common operations.                     """
    def copy(self, category, key, new_key):
        collection = self.db[category]
        result = collection.aggregate([
            {"$match": {"_id": key}},
            {"$replaceRoot": {
                "newRoot": {
                    "$mergeObjects": [
                        "$$ROOT",
                        {"id": new_key}
                    ]
                }
            }},
            {"$project": {"_id": 0, "version": 0}},
            {"$out": category}
        ])

        if len(list(result)) == 0:
            raise ValueError(f"_id {key} not found in the collection {category}.")

    def get_field(self, category: str, key: str, field: str) -> Any:
        collection = self.db[category]
        result = collection.find_one({"_id": key}, {field: 1, "_id": 0})
        if result is None:
            raise ValueError(f"_id {key} not found in the collection {category}.")
        if field not in result:
            raise KeyError(f"Key '{field}' not found in the document with _id {key}.")
        return result[field]

    def exists(self, category: str, key: str) -> bool:
        collection = self.db[category]
        return collection.count_documents({"_id": key}) > 0

    def increment(self, category: str, key: str, field: str, amount: int = 1) -> int:
        """Increment a value stored under a specified key, returning the original value."""
        collection = self.db[category]
        result = collection.find_one_and_update(
            {"_id": key},
            {"$inc": {field: amount}},
            return_document=ReturnDocument.BEFORE
        )
        if result is None:
            raise ValueError(f"_id {key} not found in the collection {category}.")
        return result.get(field, 0)

    def pop_field(self, category: str, key: str, field: str) -> Any:
        collection = self.db[category]
        result = collection.find_one_and_update(
            {"_id": key},
            {"$unset": {field: ""}},
            return_document=ReturnDocument.BEFORE
        )
        if result is None:
            raise ValueError(f"_id {key} not found in the collection {category}.")
        return result.get(field, None)



    """                     List operations                     """
    def append_to_array(self, category: str, key: str, field: str, value: Any) -> None:
        collection = self.db[category]
        result = collection.update_one(
            {"_id": key},
            {"$push": {field: value}}
        )
        if result.matched_count == 0:
            raise ValueError(f"_id {key} not found in the collection {category}.")

    def remove_from_array_at_index(self, category: str, key: str, field: str, index: int) -> None:
        collection = self.db[category]
        document = collection.find_one({"_id": key})
        if document is None:
            raise ValueError(f"_id {key} not found in the collection {category}.")
        if field not in document:
            raise KeyError(f"Field '{field}' not found in the document with _id {key}.")
        if index < 0 or index >= len(document[field]):
            raise IndexError(f"Index {index} is out of range for the array in field '{field}' of document with _id {key}.")
        
        collection.update_one(
            {"_id": key},
            {"$unset": {f"{field}.{index}": ""}}
        )
        collection.update_one(
            {"_id": key},
            {"$pull": {field: None}}
        )

    def remove_value_from_array(self, category: str, key: str, field: str, value: Any) -> None:
        collection = self.db[category]
        document = collection.find_one({"_id": key})
        if document is None:
            raise ValueError(f"_id {key} not found in the collection {category}.")
        if field not in document:
            raise KeyError(f"Field '{field}' not found in the document with _id {key}.")
        if value not in document[field]:
            raise ValueError(f"Value '{value}' not found in the array of field '{field}' in the document with _id {key}.")
        
        collection.update_one(
            {"_id": key},
            {"$pull": {field: value}}
        )

    def pop_array(self, category: str, key: str, field: str, index: int = -1) -> Any:
        collection = self.db[category]
        result = collection.find_one_and_update(
            {"_id": key},
            {"$pop": {field: 1 if index >= 0 else -1}},
            projection={field: 1, "_id": 0},
            return_document=ReturnDocument.BEFORE
        )
        if result is None:
            raise ValueError(f"_id {key} not found in the collection {category}.")
        if field not in result:
            raise KeyError(f"Field '{field}' not found in the document with _id {key}.")
        return result[field][index]

    def array_length(self, category: str, key: str, field: str) -> int:
        collection = self.db[category]
        result = collection.aggregate([
            {"$match": {"_id": key}},
            {"$project": {field: {"$size": f"${field}"}}}
        ])
        result = list(result)
        if not result:
            raise ValueError(f"_id {key} not found in the collection {category}.")
        if field not in result[0]:
            raise KeyError(f"Field '{field}' not found in the document with _id {key}.")
        return result[0][field]




    """                     Batch operations                     """
    def batch_create(self, category: str, keys: Dict[str, Dict[str, Any]]) -> None:
        try:
            collection = self.db[category]
            documents = []
            for key, value in keys.items():
                value.pop("id", None)
                document = {"_id": key, "version": 1, **value}
                documents.append(document)
            collection.insert_many(documents, ordered=False)
        except pymongo.errors.BulkWriteError as e:
            raise ValueError(f"One or more documents already exist in collection {category}.")
        except Exception as e:
            raise ValueError(f"Failed to create documents: {str(e)}")

    def batch_read(self, category: str, keys: List[str]) -> Dict[str, Dict[str, Any]]:
        collection = self.db[category]
        results = collection.find({"_id": {"$in": keys}})
        documents = {}
        for result in results:
            result_copy = result.copy()
            result_copy.pop("_id")
            result_copy.pop("version", None)
            result_copy["id"] = result["_id"]
            documents[result["_id"]] = result_copy
        return documents

    def batch_update(self, category: str, updated_fields: Dict[str, Dict[str, Any]]) -> None:
        try:
            collection = self.db[category]
            bulk_operations = []
            for key, fields in updated_fields.items():
                fields.pop("id", None)
                current_document = collection.find_one({"_id": key})
                if current_document is None:
                    raise ValueError(f"_id {key} not found in the collection {category}.")
                new_version = current_document.get("version", 0) + 1
                update_fields = {"version": new_version, **fields}
                bulk_operations.append(
                    pymongo.UpdateOne(
                        {"_id": key, "version": current_document["version"]},
                        {"$set": update_fields}
                    )
                )
            collection.bulk_write(bulk_operations)
        except pymongo.errors.BulkWriteError as e:
            raise ValueError(f"Failed to update one or more documents due to concurrent modification.")
        except Exception as e:
            raise ValueError(f"Failed to update documents: {str(e)}")

    def batch_delete(self, category: str, keys: List[str]) -> None:
        collection = self.db[category]
        result = collection.delete_many({"_id": {"$in": keys}})
        if result.deleted_count != len(keys):
            raise ValueError(f"One or more _ids not found in the collection {category}.")

    def batch_copy(self, category: str, keys: List[str], new_keys: List[str]) -> None:
        collection = self.db[category]
        bulk_operations = []
        for key, new_key in zip(keys, new_keys):
            bulk_operations.append(
                pymongo.InsertOne({
                    "$replaceRoot": {
                        "newRoot": {
                            "$mergeObjects": [
                                {"$match": {"_id": key}},
                                {"id": new_key}
                            ]
                        }
                    },
                    "$project": {"_id": 0, "version": 0},
                })
            )
        try:
            collection.bulk_write(bulk_operations, ordered=False)
        except pymongo.errors.BulkWriteError as e:
            raise ValueError(f"One or more _ids not found in the collection {category}.")