import pymongo
from pymongo import MongoClient

from swarmstar.swarm.types import SwarmConfig

mongodb_uri = "mongodb://localhost:27017/"


def get_kv(db_name: str, category: str, _id: str) -> dict:
    try:
        collection_name = category
        client = MongoClient(mongodb_uri)
        db = client[db_name]
        collection = db[collection_name]
        result = collection.find_one({"_id": _id})
        if result is None:
            raise ValueError(f"Id {_id} not found in MongoDB collection.")
        result["id"] = result.pop("_id")
        return result
    except Exception as e:
        raise ValueError(
            f"Failed to get id {_id} from MongoDB collection {collection_name} in database {db_name}"
        ) from e


def get_swarm_config(db_name: str, swarm_id: str) -> dict:
    return SwarmConfig(**get_kv(db_name, "swarm", swarm_id))
