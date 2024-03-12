from pydantic import ValidationError
from swarmstar.types import (
    SwarmConfig, 
    SwarmOperation, 
    BlockingOperation, 
    UserCommunicationOperation, 
    SpawnOperation,
    TerminationOperation,
    ActionOperation,
    FailureOperation
)
from swarmstar.utils.data import add_kv, get_kv, set_kv

def save_swarm_operation(swarm: SwarmConfig, operation: SwarmOperation) -> None:
    add_kv(swarm, "swarm_operations", operation.id, operation.model_dump())

def get_swarm_operation(swarm: SwarmConfig, operation_id: str) -> SwarmOperation:
    operation = get_kv(swarm, "swarm_operations", operation_id)
    if operation is None:
        raise ValueError(f"Operation with id {operation_id} not found")
    operation_type = operation["operation_type"]
 
    operation_mapping = {
        "blocking": BlockingOperation,
        "user_communication": UserCommunicationOperation,
        "spawn": SpawnOperation,
        "terminate": TerminationOperation,
        "action": ActionOperation,
        "node_failure": FailureOperation,
    }
    
    if operation_type in operation_mapping:
        try:
            OperationClass = operation_mapping[operation_type]
            return OperationClass.model_validate(operation)
        except ValidationError as e:
            print(f"Error validating operation {operation} of type {operation_type}")
            raise e
        except Exception as e:
            raise e
    else:
        raise ValueError(f"Operation type {operation_type} not recognized")
        


def update_swarm_operation(swarm: SwarmConfig, operation: SwarmOperation) -> None:
    set_kv(swarm, "swarm_operations", operation.id, operation.model_dump())
