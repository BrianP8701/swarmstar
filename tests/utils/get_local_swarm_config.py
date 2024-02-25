import pymongo
from pymongo import MongoClient

from swarmstar.swarm.types import SwarmConfig

mongodb_uri = "mongodb://localhost:27017/"


def create_collection(db_name: str, category: str) -> None:
    client = MongoClient(mongodb_uri)
    db = client[db_name]
    collection = db[category]
    collection.create_index([("key", pymongo.ASCENDING)], unique=True)


def get_kv(db_name: str, category: str, key: str) -> dict:
    try:
        collection_name = category
        client = MongoClient(mongodb_uri)
        db = client[db_name]
        if collection_name not in db.list_collection_names():
            create_collection(db_name, collection_name)
        collection = db[collection_name]
        result = collection.find_one({"key": key})
        if result is None:
            raise ValueError(f"Key {key} not found in MongoDB collection.")
        result.pop("_id")
        result.pop("key")

        return result
    except Exception as e:
        raise ValueError(
            f"Failed to get key {key} from MongoDB collection {collection_name} in database {db_name}"
        ) from e


def get_swarm_config(db_name: str) -> dict:
    return SwarmConfig(**get_kv(db_name, "swarm", "swarm"))
