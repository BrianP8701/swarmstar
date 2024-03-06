from swarmstar.swarm.types import SwarmConfig, SwarmNode
from swarmstar.utils.data import add_kv, get_kv, set_kv

def save_swarm_node(swarm: SwarmConfig, node: SwarmNode) -> None:
    add_kv(swarm, "swarm_nodes", node.id, node.model_dump())

def update_swarm_node(swarm: SwarmConfig, node: SwarmNode) -> None:
    set_kv(swarm, "swarm_nodes", node.id, node.model_dump())

def get_swarm_node(swarm: SwarmConfig, node_id: str) -> SwarmNode:
    node = SwarmNode.model_validate(get_kv(swarm, "swarm_nodes", node_id))
    return node
