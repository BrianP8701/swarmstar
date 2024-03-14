from typing import List

from swarmstar.utils.data import MongoDBWrapper
from swarmstar.models.swarm_node import SwarmNode

db = MongoDBWrapper()

class SwarmState:
    @staticmethod
    def add_node_id_to_swarm_state(swarm_id: str, node_id: str) -> None:
        db.append("swarm_state", swarm_id, node_id)

    @staticmethod
    def get_swarm_state(swarm_id: str) -> List[str]:
        """
        Get a list of all the node ids that are part of this swarm.
        """
        return db.get("swarm_state", swarm_id)['data']

    @staticmethod
    def get_len_swarm_state(swarm_id: str) -> int:
        return len(db.get("swarm_state", swarm_id)['data'])

    @staticmethod
    def get_swarm_node_by_index(swarm_id: str, index: int) -> SwarmNode:
        return db.get("swarm_state", swarm_id)['data'][index]
