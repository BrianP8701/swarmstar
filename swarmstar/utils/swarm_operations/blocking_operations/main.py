from importlib import import_module
from typing import List, Union
import inspect

from swarmstar.utils.swarmstar_space import add_swarm_operation_to_swarm_history, save_swarm_operation
from swarmstar.types import (
    BlockingOperation,
    SwarmConfig,
    SwarmOperation,
)


async def blocking(
    swarm_config: SwarmConfig, blocking_operation: BlockingOperation
) -> Union[SwarmOperation, List[SwarmOperation]]:
    blocking_operation_type_map = {
        "instructor_completion": "swarmstar.utils.swarm_operations.blocking_operations.instructor.completion",
        "internal_action": "swarmstar.utils.swarm_operations.blocking_operations.internal_action",
    }

    blocking_operation_type = blocking_operation.blocking_type

    if blocking_operation_type not in blocking_operation_type_map:
        raise ValueError(
            f"Blocking operation type: `{blocking_operation_type.type}` is not supported."
        )

    blocking_operation_type_module = import_module(
        blocking_operation_type_map[blocking_operation_type]
    )
    
    blocking_func = blocking_operation_type_module.blocking

    if inspect.iscoroutinefunction(blocking_func):
        output: SwarmOperation = await blocking_func(swarm_config, blocking_operation)
    else:
        output: SwarmOperation = blocking_func(swarm_config, blocking_operation)

    save_swarm_operation(swarm_config, blocking_operation)
    add_swarm_operation_to_swarm_history(swarm_config, blocking_operation.id)
    
    return output
