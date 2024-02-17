from typing import Any, Dict, Union
from importlib import import_module

from swarm_star.swarm.types import SwarmConfig, SwarmOperation, BlockingOperation, ActionSpace, SwarmHistory

def execute_blocking_operation(swarm: SwarmConfig, blocking_operation: BlockingOperation) -> SwarmOperation:
    blocking_operation_type_map = {
        'openai_instructor_completion': 'swarm_star.utils.swarm_utils.blocking_operations.openai_instructor_completion',
        'internal_action': 'swarm_star.utils.swarm_utils.blocking_operations.internal_action'
    }
    
    blocking_operation_type = blocking_operation.type
    
    if blocking_operation_type not in blocking_operation_type_map:
        raise ValueError(f"Blocking operation type: `{blocking_operation_type.type}` is not supported.")
    else:
        pass
    
    blocking_operation_type_module = import_module(blocking_operation_type_map[blocking_operation_type])
    
    blocking_operation_output = blocking_operation_type_module.execute_blocking_operation(swarm, blocking_operation)
    swarm_history = SwarmHistory(swarm=swarm)
    swarm_history.add_event(blocking_operation)
    
    return blocking_operation_output