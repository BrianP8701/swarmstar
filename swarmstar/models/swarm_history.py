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
        db.append_to_list("admin", swarm_id, "swarm_history", swarm_operation_id)

    @staticmethod
    def get(swarm_id: str) -> List[str]:
        """
        Get the swarm history for a given swarm id.
        """
        return db.get_by_key("admin", swarm_id, "swarm_history")
