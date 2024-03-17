from typing import List

from swarmstar.utils.data import MongoDBWrapper
from swarmstar.models import SwarmOperation

db = MongoDBWrapper()


class SwarmHistory:
    @staticmethod
    def append(swarm_id, swarm_operation_id: str) -> None:
        """
            Add a swarm operation id to the swarm history when 
            a swarm operation is executed.
        """
        db.append_to_list("swarm_history", swarm_id, "data", swarm_operation_id)

    @staticmethod
    def get(swarm_id: str) -> List[str]:
        """
        Get the swarm history for a given swarm id.
        """
        return db.get("swarm_history", swarm_id)["data"]

    @staticmethod
    def save(swarm_id: str, swarm_operation_ids: List[str]) -> None:
        """
        Insert a new swarm history into the swarm history collection.
        """
        db.insert("swarm_history", swarm_id, {"data": swarm_operation_ids})
