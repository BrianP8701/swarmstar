from swarmstar.swarm.types.swarm_config import SwarmConfig
from swarmstar.swarm.types.swarm_nodes import SwarmNode
from swarmstar.utils.data import add_kv, get_kv, set_kv, append_to_list

def add_node_to_swarm_state(swarm: SwarmConfig, node: SwarmNode) -> None:
    add_kv(swarm, "swarm_state", node.id, node.model_dump())
    append_to_list(swarm, "swarm_state", swarm.swarm_id, node.id)

def get_node_from_swarm_state(swarm: SwarmConfig, node_id: str) -> SwarmNode:
    node = SwarmNode.model_validate(get_kv(swarm, "swarm_state", node_id))
    return node

def set_node_in_swarm_state(swarm: SwarmConfig, node: SwarmNode) -> None:
    set_kv(swarm, "swarm_state", node.id, node.model_dump())
