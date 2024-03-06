"""
The swarm state contains a list of all the
node ids that are part of a swarm.
"""
from typing import List

from swarmstar.swarm.types.swarm_config import SwarmConfig
from swarmstar.swarm.types.swarm_node import SwarmNode
from swarmstar.utils.data import get_kv, append_to_list

def add_node_to_swarm_state(swarm: SwarmConfig, node: SwarmNode) -> None:
    append_to_list(swarm, "swarm_state", swarm.swarm_id, "data", node.id)

def get_swarm_state(swarm: SwarmConfig, node_id: str) -> List[str]:
    return get_kv(swarm, "swarm_state", swarm.swarm_id)['data']

def get_len_swarm_state(swarm: SwarmConfig) -> int:
    return len(get_kv(swarm, "swarm_state", swarm.swarm_id)['data'])

def get_swarm_node_by_index(swarm: SwarmConfig, index: int) -> SwarmNode:
    return get_kv(swarm, "swarm_state", swarm.swarm_id)['data'][index]
