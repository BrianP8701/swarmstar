from importlib import import_module
from typing import Union

from swarmstar.utils.swarmstar_space import get_swarm_node
from swarmstar.types import (
    SwarmConfig,
    TerminationOperation,
)

def terminate(
    swarm: SwarmConfig, termination_operation: TerminationOperation
) -> Union[TerminationOperation, None]:
    termination_policy_map = {
        "simple": "swarmstar.utils.swarm_operations.termination_operations.simple",
        "parallel_review": "swarmstar.utils.swarm_operations.termination_operations.parallel_review",
        "clone_with_questions_answered": "swarmstar.utils.swarm_operations.termination_operations.clone_with_questions_answered",
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
    
    try:
        output = termination_policy_module.terminate(swarm, termination_operation)
    except Exception as e:
        print(f"Error in termination policy module: {e}")
        output = None
    
    return output