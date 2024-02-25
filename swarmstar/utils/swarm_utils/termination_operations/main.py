from importlib import import_module
from typing import Union

from swarmstar.swarm.types import (
    SwarmConfig,
    SwarmHistory,
    SwarmState,
    TerminationOperation,
)


def terminate(
    swarm: SwarmConfig, termination_operation: TerminationOperation
) -> Union[TerminationOperation, None]:
    termination_policy_map = {
        "simple": "swarmstar.utils.swarm_utils.termination_operations.simple",
        "parallel_review": "swarmstar.utils.swarm_utils.termination_operations.parallel_review",
        "clone_with_questions_answered": "swarmstar.utils.swarm_utils.termination_operations.clone_with_questions_answered",
    }

    swarm_state = SwarmState(swarm=swarm)
    node_id = termination_operation.node_id
    node = swarm_state[node_id]
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
    swarm_history = SwarmHistory(swarm=swarm)
    swarm_history.add_event(termination_operation)

    return output
