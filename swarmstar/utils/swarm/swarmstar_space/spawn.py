"""
This module is responsible for preparing mongoDB for a new swarmstar space.
"""
from swarmstar.swarm.types.swarm_config import SwarmConfig
from swarmstar.utils.data import add_kv, append_to_list

def spawn_starswarm_space(swarm: SwarmConfig, swarm_id: str) -> None:
    add_kv(swarm, "swarm_operations", swarm_id, {"data": []})
    add_kv(swarm, "swarm_nodes", swarm_id, {"data": []})
    append_to_list(swarm, "admin", "swarms", "data", swarm.swarm_id)