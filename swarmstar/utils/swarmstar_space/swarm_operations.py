from swarmstar.types import SwarmConfig, SwarmOperation
from swarmstar.utils.data import add_kv, get_kv

def save_swarm_operation(swarm: SwarmConfig, operation: SwarmOperation) -> None:
    add_kv(swarm, "swarm_operations", operation.id, operation.model_dump())

def get_swarm_operation(swarm: SwarmConfig, operation_id: str) -> SwarmOperation:
    operation = SwarmOperation.model_validate(get_kv(swarm, "swarm_operations", operation_id))
    return operation
