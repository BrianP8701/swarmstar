from typing import List, Union
import inspect

from swarmstar.models import (
    SwarmConfig,
    SwarmOperation,
    SpawnOperation,
    NodeEmbryo,
    Swarmstar,
    SwarmHistory
)
from swarmstar.utils.swarm_operations import (
    blocking,
    failure,
    spawn,
    terminate,
    execute_action
)

def spawn_swarm(swarm_config: SwarmConfig, goal: str) -> SpawnOperation:
    """
    Create the first spawn operation for the swarm.
    """
    Swarmstar.spawn_swarmstar_space(swarm_config)
    
    root_spawn_operation = SpawnOperation(
        node_embryo=NodeEmbryo(
            action_id='swarmstar/actions/reasoning/decompose_directive',
            message=goal
        )
    )
    
    SwarmOperation.insert_swarm_operation(root_spawn_operation)
    return root_spawn_operation


async def execute_swarmstar_operation(
    swarm_config: SwarmConfig, swarm_operation: SwarmOperation
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
        "action": execute_action,
    }

    if swarm_operation.operation_type in operation_mapping:
        try:
            operation_func = operation_mapping[swarm_operation.operation_type]
            
            if inspect.iscoroutinefunction(operation_func):
                output = await operation_func(swarm_config, swarm_operation)
            else:
                output = operation_func(swarm_config, swarm_operation)        
        except Exception as e:
            print(f"Error in execute_swarmstar_operation: {e}")
            raise e
    else:
        raise ValueError(
            f"Unknown swarm operation type: {swarm_operation.operation_type}"
        )
    
    if output is None:
        return None
    elif isinstance(output, SwarmOperation):
        output = [output]
    elif not isinstance(output, list):
        raise ValueError(f"Unexpected return type from operation_func: {type(output)}")

    for operation in output:
        # Insert new operations into the swarm operations collection
        SwarmOperation.insert_swarm_operation(operation)

    # Add executed operation to swarm history
    SwarmHistory.add_swarm_operation_id_to_swarm_history(swarm_config.id, swarm_operation.id)

    return output