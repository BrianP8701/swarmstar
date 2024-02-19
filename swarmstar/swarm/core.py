from typing import List, Union

from swarmstar.swarm.types import SwarmConfig, SwarmOperation, SpawnOperation, NodeEmbryo
from swarmstar.utils.swarm_utils.spawn_operations.main import execute_spawn_operation
from swarmstar.utils.swarm_utils.blocking_operations.main import execute_blocking_operation
from swarmstar.utils.swarm_utils.termination_operations.main import execute_termination_operation
from swarmstar.utils.swarm_utils.failure_operations.main import execute_failure_operation

def create_first_spawn_operation(goal: str) -> SpawnOperation:
    return SpawnOperation(
        operation_type='spawn',
        node_embedding=[
            NodeEmbryo(
                action_id='swarmstar/actions/reasoning/decompose_directive',
                message=goal
            )
        ]
    )

def execute_swarm_operation(swarm: SwarmConfig, swarm_operation: SwarmOperation) -> Union[List[SwarmOperation], None]:
    if swarm_operation.operation_type == 'spawn':
        output = execute_spawn_operation(swarm, swarm_operation)
    elif swarm_operation.operation_type == 'blocking_operation':
        output = execute_blocking_operation(swarm, swarm_operation)
    elif swarm_operation.operation_type == 'terminate':
        output = execute_termination_operation(swarm, swarm_operation)
    elif swarm_operation.operation_type == 'node_failure':
        output = execute_failure_operation(swarm, swarm_operation)
    else:
        raise ValueError(f"Unknown swarm operation type: {swarm_operation.operation_type}")
    
    if not isinstance(output, list) and output is not None:
        output = [output]
    return output
