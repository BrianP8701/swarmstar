from typing import List

from swarmstar.utils.data import MongoDBWrapper
from swarmstar.models.swarm_node import SwarmNode

db = MongoDBWrapper()

class SwarmState:
    @staticmethod
    def append(swarm_id: str, node_id: str) -> None:
        """
        Append a new node to the swarm state.
        """
        db.append_to_list("swarm_state", swarm_id, "data", node_id)

    @staticmethod
    def get(swarm_id: str) -> List[str]:
        """
        Get a list of all the node ids that are part of this swarm.
        """
        return db.get("swarm_state", swarm_id)["data"]

    @staticmethod
    def save(swarm_id: str, swarm_state: List[str]) -> None:
        """
        Insert a new swarm state into the swarm state collection.
        """
        db.insert("swarm_state", swarm_id, {"data": swarm_state})
        
