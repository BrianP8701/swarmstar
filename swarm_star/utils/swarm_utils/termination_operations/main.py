from importlib import import_module
from typing import Union

from swarm_star.swarm.types import SwarmConfig, SwarmOperation, TerminationOperation, SwarmHistory, SwarmState

def execute_termination_operation(swarm: SwarmConfig, termination_operation: TerminationOperation) -> Union[SwarmOperation, None]:
    termination_policy_map = {
        'leaf': 'swarm_star.utils.swarm_utils.termination_operations.leaf',
        'simple': 'swarm_star.utils.swarm_utils.termination_operations.simple',
        'parallel_review': 'swarm_star.utils.swarm_utils.termination_operations.parallel_review',
        'clone_with_reports': 'swarm_star.utils.swarm_utils.termination_operations.clone_with_reports'
    }
    
    swarm_state = SwarmState(swarm=swarm)
    node_id = termination_operation.node_id
    node = swarm_state[node_id]
    termination_policy = node.termination_policy
    
    if termination_policy not in termination_policy_map:
        raise ValueError(f"Termination policy: `{termination_policy}` is not supported.")
    else:
        pass
    
    termination_policy_module = import_module(termination_policy_map[termination_policy])
    
    termination_operation_output = termination_policy_module.execute_termination_operation(swarm, termination_operation)
    swarm_history = SwarmHistory(swarm=swarm)
    swarm_history.add_event(termination_operation)
    
    return termination_operation_output
