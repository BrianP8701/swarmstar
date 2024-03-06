import pymongo
from pymongo import MongoClient

from swarmstar.types import SwarmConfig, SwarmNode
from swarmstar.utils.swarm.swarmstar_space import get_swarm_node, add_node_to_swarm_state

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


def get_swarm_config(db_name: str) -> dict:
    return SwarmConfig(**get_kv(db_name, "config", "swarm_config"))


swarm_config = get_swarm_config("0")

temp_node = SwarmNode(
    parent_id="0",
    action_id="0",
    message="This is a test message",
    termination_policy="simple",
)
print('\n\n\n\n\n')

print(temp_node)
add_node_to_swarm_state(swarm_config, temp_node)

retrieved_node = get_swarm_node(swarm_config, temp_node.id)
print('\n\n\n\n\n')
print(retrieved_node)
print('\n\n\n\n\n')
