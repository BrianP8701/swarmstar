from typing import List, Union

from swarmstar.swarm.types import SwarmConfig, SwarmOperation
from swarmstar.utils.swarm_utils.spawn_operations.main import spawn
from swarmstar.utils.swarm_utils.blocking_operations.main import blocking
from swarmstar.utils.swarm_utils.termination_operations.main import terminate
from swarmstar.utils.swarm_utils.failure_operations.main import failure
from swarmstar.swarm.decorators import swarmstar_decorator

def swarmstar_god(swarm: SwarmConfig, swarm_operation: SwarmOperation) -> Union[List[SwarmOperation], None]:
    if swarm_operation.operation_type == 'spawn':
        output = spawn(swarm, swarm_operation)
    elif swarm_operation.operation_type == 'blocking':
        output = blocking(swarm, swarm_operation)
    elif swarm_operation.operation_type == 'terminate':
        output = terminate(swarm, swarm_operation)
    elif swarm_operation.operation_type == 'node_failure':
        output = failure(swarm, swarm_operation)
    else:
        raise ValueError(f"Unknown swarm operation type: {swarm_operation.operation_type}")
    
    if not isinstance(output, list) and output is not None:
        output = [output]
    return output
