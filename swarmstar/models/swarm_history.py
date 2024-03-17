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
        db.append("swarm_history", swarm_id, "data", swarm_operation_id)

    @staticmethod
    def get(swarm_id: str) -> List[str]:
        return db.get("swarm_history", swarm_id)["data"]

    @staticmethod
    def get_len(swarm_id: str) -> int:
        return len(db.get("swarm_history", swarm_id)["data"])

    @staticmethod
    def get_by_index(swarm_id: str, index: int) -> SwarmOperation:
        return db.get("swarm_history", swarm_id)["data"][index]

    @staticmethod
    def add(swarm_id: str, swarm_operaion_ids: List[str]) -> None:
        db.insert("swarm_history", swarm_id, {"data": swarm_operaion_ids})