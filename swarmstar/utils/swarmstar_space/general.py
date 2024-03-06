"""
This module is responsible for preparing mongoDB for a new swarmstar space.
"""
from swarmstar.types.swarm_config import SwarmConfig
from swarmstar.utils.data import add_kv, append_to_list, delete_kv, get_kv, set_kv
from swarmstar.utils.swarmstar_space.swarm_state import get_swarm_state
from swarmstar.utils.swarmstar_space.swarm_history import get_swarm_history


def spawn_swarmstar_space(swarm_config: SwarmConfig) -> None:
    add_kv(swarm_config, "swarm_history", swarm_config.id, {"data": []})
    add_kv(swarm_config, "swarm_state", swarm_config.id, {"data": []})
    add_kv(swarm_config, "config", swarm_config.id, swarm_config.model_dump())
    append_to_list(swarm_config, "admin", "swarms", "data", swarm_config.id)

def delete_swarmstar_space(swarm_config: SwarmConfig) -> None:
    swarm_node_ids = get_swarm_state(swarm_config)
    for swarm_node_id in swarm_node_ids:
        delete_kv(swarm_config, "swarm_nodes", swarm_node_id)
    
    swarm_operation_ids = get_swarm_history(swarm_config)
    for swarm_operation_id in swarm_operation_ids:
        delete_kv(swarm_config, "swarm_operations", swarm_operation_id)
    
    delete_kv(swarm_config, "config", swarm_config.id)
    delete_kv(swarm_config, "memory_space", swarm_config.id)
    delete_kv(swarm_config, "action_space", swarm_config.id)
    delete_kv(swarm_config, "util_space", swarm_config.id)
    delete_kv(swarm_config, "swarm_state", swarm_config.id)
    delete_kv(swarm_config, "swarm_history", swarm_config.id)

    admin_swarm_id_list = get_kv(swarm_config, "admin", "swarms")["data"]
    admin_swarm_id_list.remove(swarm_config.id)
    set_kv(swarm_config, "admin", "swarms", "data", admin_swarm_id_list)
