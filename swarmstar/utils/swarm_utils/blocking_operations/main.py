from importlib import import_module
from typing import List, Union

from swarmstar.swarm.types import (
    BlockingOperation,
    SwarmConfig,
    SwarmHistory,
    SwarmOperation,
)


def blocking(
    swarm: SwarmConfig, blocking_operation: BlockingOperation
) -> Union[SwarmOperation, List[SwarmOperation]]:
    blocking_operation_type_map = {
        "instructor_completion": "swarmstar.utils.swarm_utils.blocking_operations.instructor.completion",
        "internal_action": "swarmstar.utils.swarm_utils.blocking_operations.internal_action",
    }

    blocking_operation_type = blocking_operation.blocking_type

    if blocking_operation_type not in blocking_operation_type_map:
        raise ValueError(
            f"Blocking operation type: `{blocking_operation_type.type}` is not supported."
        )

    blocking_operation_type_module = import_module(
        blocking_operation_type_map[blocking_operation_type]
    )
    output: SwarmOperation = blocking_operation_type_module.blocking(
        swarm, blocking_operation
    )

    swarm_history = SwarmHistory(swarm=swarm)
    swarm_history.add_event(blocking_operation)

    return output
