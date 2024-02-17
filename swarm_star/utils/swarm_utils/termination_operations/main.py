from importlib import import_module
from typing import Any, Dict, Union

from swarm_star.swarm.types import SwarmConfig, SwarmOperation, TerminationOperation, SwarmHistory

def execute_termination_operation(swarm: SwarmConfig, termination_operation: TerminationOperation) -> SwarmOperation:
    termination_operation_type_map = {
        'simple_termination': 'swarm_star.utils.swarm_utils.termination_operations.simple_termination',
        'parallel_review_termination': 'swarm_star.utils.swarm_utils.termination_operations.parallel_review_termination',
        'clone_with_reports': 'swarm_star.utils.swarm_utils.termination_operations.recursive_self_spawn_termination'
    }
    
    termination_operation_type = termination_operation.type
    
    if termination_operation_type not in termination_operation_type_map:
        raise ValueError(f"Termination operation type: `{termination_operation_type.type}` is not supported.")
    else:
        pass
    
    termination_operation_type_module = import_module(termination_operation_type_map[termination_operation_type])
    
    termination_operation_output = termination_operation_type_module.execute_termination_operation(swarm, termination_operation)
    swarm_history = SwarmHistory(swarm=swarm)
    swarm_history.add_event(termination_operation)
    
    return termination_operation_output