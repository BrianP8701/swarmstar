from typing import List

from swarmstar.database import MongoDBWrapper

db = MongoDBWrapper()

class SwarmState:
    @staticmethod
    def append(swarm_id: str, node_id: str) -> None:
        """
        Append a new node to the swarm state.
        """
        db.append_to_list("admin", swarm_id, "swarm_state", node_id)

    @staticmethod
    def get(swarm_id: str) -> List[str]:
        """
        Get a list of all the node ids that are part of this swarm.
        """
        return db.get_by_key("admin", swarm_id, "swarm_state")
