"""
The swarm history contains a list of swarm operations ids 
for each swarm id in chronological order.
"""
from typing import List

from swarmstar.swarm.types import SwarmConfig, SwarmOperation
from swarmstar.utils.data import get_kv, append_to_list

def add_event_to_swarm_history(swarm: SwarmConfig, swarm_operation_id: str) -> None:
    append_to_list(swarm, "swarm_history", swarm.swarm_id, "data", swarm_operation_id)
    
def get_swarm_history(swarm: SwarmConfig) -> List[str]:
    return get_kv(swarm, "swarm_history", swarm.swarm_id)["data"]

def get_len_swarm_history(swarm: SwarmConfig) -> int:
    return len(get_kv(swarm, "swarm_history", swarm.swarm_id)["data"])

def get_swarm_operation_by_index(swarm: SwarmConfig, index: int) -> SwarmOperation:
    return get_kv(swarm, "swarm_history", swarm.swarm_id)["data"][index]
