"""
Nodes can perform 1 of 5 "SwarmOperations":
    - SpawnOperation
    - ActionOperation
    - TerminationOperation
    - BlockingOperation
    - UserCommunicationOperation
"""
from __future__ import annotations
from typing import Any, Dict, Literal, Optional, Union, List
from pydantic import BaseModel, Field
from pydantic import ValidationError

from swarmstar.utils.misc.generate_uuid import generate_uuid
from swarmstar.utils.database import MongoDBWrapper
from swarmstar.utils.misc.get_next_available_id import get_available_id

db = MongoDBWrapper()

class SwarmOperation(BaseModel):
    id: Optional[str] = Field(default_factory=lambda: get_available_id("swarm_operations"))
    operation_type: Literal[
        "spawn",
        "terminate",
        "blocking",
        "user_communication",
        "action"
    ]

    @classmethod
    def model_validate(cls,data: Union[Dict[str, Any], 'SwarmOperation'], **kwargs) -> 'SwarmOperation':
        if isinstance(data, SwarmOperation):
            return data
        elif isinstance(data, dict):
            operation_type = data.get('operation_type')
            operation_mapping = {
                "blocking": BlockingOperation,
                "user_communication": UserCommunicationOperation,
                "spawn": SpawnOperation,
                "terminate": TerminationOperation,
                "action": ActionOperation
            }
            return operation_mapping[operation_type].model_validate(**data)
        return super().model_validate(data, **kwargs)

    @staticmethod
    def save(operation: SwarmOperation) -> None:
        db.insert("swarm_operations", operation.id, operation.model_dump())

    @staticmethod
    def replace(operation: SwarmOperation) -> None:
        db.replace("swarm_operations", operation.id, operation.model_dump())

    @staticmethod
    def get(operation_id: str) -> SwarmOperation:
        operation = db.get("swarm_operations", operation_id)
        if operation is None:
            raise ValueError(f"Operation with id {operation_id} not found")
        operation_type = operation["operation_type"]
    
        operation_mapping = {
            "blocking": BlockingOperation,
            "user_communication": UserCommunicationOperation,
            "spawn": SpawnOperation,
            "terminate": TerminationOperation,
            "action": ActionOperation
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

    @staticmethod
    def delete(operation_id: str) -> None:
        db.delete("swarm_operations", operation_id)

    @staticmethod
    def clone(operation_id: str, new_swarm_id: str) -> None:
        operation = SwarmOperation.get(operation_id)
        parts = operation.id.split("_", 1)
        operation.id = f"{new_swarm_id}_{parts[1]}"
        operation.save()


class BlockingOperation(SwarmOperation):
    operation_type: Literal["blocking"] = Field(default="blocking")
    node_id: str
    blocking_type: Literal[
        "instructor_completion",
        "openai_completion"
    ]
    args: Dict[str, Any] = {}
    context: Dict[str, Any] = {}
    next_function_to_call: str

class SpawnOperation(SwarmOperation):
    operation_type: Literal["spawn"] = Field(default="spawn")
    action_id: str
    message: Union[str, Dict[str, Any]]
    context: Optional[Dict[str, Any]] = {}
    parent_id: Optional[str] = None
    node_id: Optional[str] = None

class ActionOperation(SwarmOperation):
    operation_type: Literal["action"] = Field(default="action")
    function_to_call: str
    node_id: str
    args: Dict[str, Any] = {}

class TerminationOperation(SwarmOperation):
    operation_type: Literal["terminate"] = Field(default="terminate")
    terminator_id: str
    node_id: str
    context: Optional[Dict[str, Any]] = None

class UserCommunicationOperation(SwarmOperation):
    operation_type: Literal["user_communication"] = Field(default="user_communication")
    node_id: str
    message: str
    context: Optional[Dict[str, Any]] = {}
    next_function_to_call: str
