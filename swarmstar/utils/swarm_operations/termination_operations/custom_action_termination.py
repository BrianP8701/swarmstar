"""
This termination operation will:
    1. Check the target node's execution memory for __termination_handler__.
    2. Call this function with the terminator node's id and the termination operation's context.
    3. Return the output of the function.
"""
from typing import Union

from swarmstar.utils.swarmstar_space import get_swarm_node
from swarmstar.types import (
    SwarmConfig,
    TerminationOperation,
    ActionOperation
)

def terminate(
    swarm_config: SwarmConfig, termination_operation: TerminationOperation
) -> Union[TerminationOperation, None]:
    terminator_node_id = termination_operation.terminator_node_id
    node_id = termination_operation.node_id
    context = termination_operation.context

    target_node = get_swarm_node(swarm_config, node_id)
    termination_handler = target_node.execution_memory.get("__termination_handler__")
    
    if termination_handler is not None:
        return ActionOperation(
            node_id=node_id,
            function_to_call=termination_handler,
            args={"terminator_node_id": terminator_node_id, "context": context},
        )

    raise ValueError(
        f"Termination handler not found in target node's execution memory. node_id: {node_id}"
    )
