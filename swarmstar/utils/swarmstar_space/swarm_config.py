from pymongo import MongoClient

from swarmstar.utils.data import add_kv, append_to_list
from swarmstar.types import SwarmConfig

def add_swarm_config(swarm_config: SwarmConfig) -> None:
    add_kv(swarm_config, "config", swarm_config.id, swarm_config.model_dump())
    append_to_list(swarm_config, "admin", "swarms", "data", swarm_config.id)

def get_swarm_config(mongodb_uri: str, db_name: str, swarm_config_id: str) -> SwarmConfig:
    return SwarmConfig(**get_kv(mongodb_uri, db_name, "config", swarm_config_id))

def get_kv(mongodb_uri: str, db_name: str, category: str, _id: str) -> dict:
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
