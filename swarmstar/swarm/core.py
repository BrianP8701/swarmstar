from typing import List, Union

from swarmstar.swarm.types import SwarmConfig, SwarmOperation, SpawnOperation, NodeEmbryo
from swarmstar.utils.swarm.operations.blocking_operations.main import blocking
from swarmstar.utils.swarm.operations.failure_operations.main import failure
from swarmstar.utils.swarm.operations.spawn_operations.main import spawn
from swarmstar.utils.swarm.operations.termination_operations.main import terminate
from swarmstar.utils.misc.uuid import generate_uuid
from swarmstar.utils.data import append_to_list
from swarmstar.utils.swarm.swarmstar_space.swarm_state import add_operation_id_to_node

 
def spawn_swarm(swarm: SwarmConfig, goal: str) -> [SwarmConfig, SpawnOperation]:
    """
    Create the first spawn operation for the swarm.
    """
    swarm_id = generate_uuid("swarmstar")
    swarm.swarm_id = swarm_id
    append_to_list(swarm, "admin", "swarms", "data", swarm_id)
    
    root_spawn_operation = SpawnOperation(
        node_embryo=NodeEmbryo(
            action_id='swarmstar/actions/reasoning/decompose_directive',
            message=goal
        )
    )
    
    return swarm, root_spawn_operation

def execute_swarmstar_operation(
    swarm: SwarmConfig, swarm_operation: SwarmOperation
) -> Union[List[SwarmOperation], None]:
    """
    This function is the main entry point for the swarmstar library. It takes in a swarm configuration and a swarm operation
    and returns a list of swarm operations that should be executed next.
    """
    operation_mapping = {
        "spawn": spawn,
        "blocking": blocking,
        "terminate": terminate,
        "node_failure": failure,
    }

    if swarm_operation.operation_type in operation_mapping:
        output = operation_mapping[swarm_operation.operation_type](
            swarm, swarm_operation
        )
    else:
        raise ValueError(
            f"Unknown swarm operation type: {swarm_operation.operation_type}"
        )
    if isinstance(output, tuple):
        output = list(output)
    if not isinstance(output, list) and output is not None:
        output = [output]
    
    add_operation_id_to_node(swarm, swarm_operation.node_id, swarm_operation.operation_id)
    return output
