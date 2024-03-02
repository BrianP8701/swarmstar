from swarmstar.swarm.types import SwarmConfig, SwarmOperation
from swarmstar.utils.data import add_kv, get_kv, append_to_list

def add_event_to_swarm_history(swarm: SwarmConfig, event: SwarmOperation) -> None:
    add_kv(swarm, "swarm_history", event.id, event.model_dump())
    append_to_list(swarm, "swarm_history", swarm.swarm_id, event.id)
    
def get_event_from_swarm_history(swarm: SwarmConfig, event_id: str) -> SwarmOperation:
    event = SwarmOperation.model_validate(get_kv(swarm, "swarm_history", event_id))
    return event
