"""
For simplicity, swarm nodes, operation, memory and action metadata have ids like:

    {swarm_id}_{x}{y}
    
Where x represents the type of node,
    o: swarm operation
    n: swarm node
    m: memory metadata
    a: action metadata

And y represents the number of the node of that type.
"""
import uuid

from swarmstar.utils.database import MongoDBWrapper
from swarmstar.context import swarm_id_var

db = MongoDBWrapper()

def generate_uuid(identifier: str) -> str:
    id = str(uuid.uuid4())
    return f"{identifier}_{id}"

def copy_under_new_swarm_id(old_id: str, new_swarm_id: str) -> str:
    if old_id[0] == "_": return old_id # Internal ids should not be copied
    retain_this_part = old_id.split("_", 1)[1]
    return f"{new_swarm_id}_{retain_this_part}"

def get_available_id(collection: str) -> str:
    if collection == "swarm_nodes": 
        x = "n"
        inner_key = "node_count"
    elif collection == "swarm_operations": 
        x = "o"
        inner_key = "operation_count"
    elif collection == "memory_metadata": 
        x = "m"
        inner_key = "memory_count"
    elif collection == "action_metadata": 
        x = "a"
        inner_key = "action_count"
    else: raise ValueError(f"Collection {collection} not recognized.")

    y = db.get_field("admin", swarm_id_var.get(), inner_key)
    db.increment("admin", swarm_id_var.get(), inner_key)
    return f"{swarm_id_var.get()}_{x}{y}"

def get_x_given_collection(collection: str) -> str:
    if collection == "swarm_nodes": return "n"
    elif collection == "swarm_operations": return "o"
    elif collection == "memory_metadata": return "m"
    elif collection == "action_metadata": return "a"
    else: raise ValueError(f"Collection {collection} not recognized.")
