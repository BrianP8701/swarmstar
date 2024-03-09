"""
The swarm state contains a list of all the
node ids that are part of a swarm.
"""
from typing import List

from swarmstar.types.swarm_config import SwarmConfig
from swarmstar.types.swarm_node import SwarmNode
from swarmstar.utils.data import get_kv, append_to_list

def add_node_id_to_swarm_state(swarm: SwarmConfig, node_id: str) -> None:
    append_to_list(swarm, "swarm_state", swarm.id, "data", node_id)

def get_swarm_state(swarm: SwarmConfig) -> List[str]:
    """
    Get a list of all the node ids that are part of this swarm.
    """
    return get_kv(swarm, "swarm_state", swarm.id)['data']

def get_len_swarm_state(swarm: SwarmConfig) -> int:
    return len(get_kv(swarm, "swarm_state", swarm.id)['data'])

def get_swarm_node_by_index(swarm: SwarmConfig, index: int) -> SwarmNode:
    return get_kv(swarm, "swarm_state", swarm.id)['data'][index]
