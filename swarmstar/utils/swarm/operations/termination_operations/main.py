from importlib import import_module
from typing import Union

from swarmstar.utils.swarm.swarmstar_space import get_swarm_node, add_swarm_operation_to_swarm_history, save_swarm_operation
from swarmstar.types import (
    SwarmConfig,
    TerminationOperation,
)


def terminate(
    swarm: SwarmConfig, termination_operation: TerminationOperation
) -> Union[TerminationOperation, None]:
    termination_policy_map = {
        "simple": "swarmstar.utils.swarm.operations.termination_operations.simple",
        "parallel_review": "swarmstar.utils.swarm.operations.termination_operations.parallel_review",
        "clone_with_questions_answered": "swarmstar.utils.swarm.operations.termination_operations.clone_with_questions_answered",
    }

    node_id = termination_operation.node_id
    node = get_swarm_node(swarm, node_id)
    termination_policy = node.termination_policy

    if termination_policy not in termination_policy_map:
        raise ValueError(
            f"Termination policy: `{termination_policy}` is not supported."
        )
    else:
        pass

    termination_policy_module = import_module(
        termination_policy_map[termination_policy]
    )

    output = termination_policy_module.terminate(swarm, termination_operation)
    
    save_swarm_operation(swarm, output)
    add_swarm_operation_to_swarm_history(swarm, termination_operation.id)

    return output
