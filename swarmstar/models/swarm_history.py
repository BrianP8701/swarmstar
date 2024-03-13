from typing import List

from swarmstar.utils.data import MongoDBWrapper
from swarmstar.models.internal_metadata import SwarmstarInternal
from swarmstar.models import SwarmOperation

db = MongoDBWrapper()
ss_internal = SwarmstarInternal()


class SwarmHistory:
    @staticmethod
    def add_swarm_operation_id_to_swarm_history(swarm_id, swarm_operation_id: str) -> None:
        """
            Add a swarm operation id to the swarm history when 
            a swarm operation is executed.
        """
        db.append("swarm_history", swarm_id, swarm_operation_id)

    @staticmethod
    def get_swarm_history(swarm_id: str) -> List[str]:
        return db.get("swarm_history", swarm_id)["data"]

    @staticmethod
    def get_len_swarm_history(swarm_id: str) -> int:
        return len(db.get("swarm_history", swarm_id)["data"])

    @staticmethod
    def get_swarm_operation_by_index(swarm_id: str, index: int) -> SwarmOperation:
        return db.get("swarm_history", swarm_id)["data"][index]
