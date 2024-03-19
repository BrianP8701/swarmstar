from typing import List

from swarmstar.utils.data import MongoDBWrapper
from swarmstar.models import SwarmOperation

db = MongoDBWrapper()


class SwarmHistory:
    @staticmethod
    def append(swarm_id, swarm_operation_id: str) -> None:
        """
            Add a swarm operation id to the swarm history when a swarm operation is executed.
        """
        db.append_to_list("admin", swarm_id, "swarm_history", swarm_operation_id)

    @staticmethod
    def get(swarm_id: str) -> List[str]:
        """
        Get a list of swarm operation ids that have been executed on the swarm.
        """
        return db.get_by_key("admin", swarm_id, "swarm_history")

    @staticmethod
    def save(swarm_id: str, swarm_history: List[str]) -> None:
        """
        Save the swarm history to the database for a new swarm.
        """
        db.update("admin", swarm_id, {"swarm_history": swarm_history})