from swarmstar.models.swarm_config import SwarmConfig
from swarmstar.models.swarm_history import SwarmHistory
from swarmstar.models.swarm_state import SwarmState
from swarmstar.utils.data import MongoDBWrapper

db = MongoDBWrapper()

class Swarmstar:
    @staticmethod
    def spawn_swarmstar_space(swarm_config: SwarmConfig) -> None:
        swarm_id = swarm_config.id
        db.add("swarm_history", swarm_id, {"data": []})
        db.add("swarm_state", swarm_id, {"data": []})
        db.add("config", swarm_id, swarm_config.model_dump())
        db.append("admin", "swarms", swarm_id)

    @staticmethod
    def delete_swarmstar_space(swarm_id: str) -> None:
        swarm_node_ids = SwarmState.get_swarm_state(swarm_id)
        for swarm_node_id in swarm_node_ids:
            db.delete("swarm_nodes", swarm_node_id)
        
        swarm_operation_ids = SwarmHistory.get_swarm_history(swarm_id)
        for swarm_operation_id in swarm_operation_ids:
            db.delete("swarm_operations", swarm_operation_id)
        
        db.delete("config", swarm_id)
        db.delete("swarm_state", swarm_id)
        db.delete("swarm_history", swarm_id)
        
        admin = db.get("admin", "swarms")
        admin["data"].remove(swarm_id)
        admin = db.get("admin", "swarms")
        admin["data"].remove(swarm_id)
        db.set("admin", "swarms", admin)
