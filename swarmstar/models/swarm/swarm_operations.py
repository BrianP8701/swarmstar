"""
Nodes can perform 1 of 5 "SwarmOperations":
    - SpawnOperation
    - ActionOperation
    - TerminationOperation
    - BlockingOperation
    - UserCommunicationOperation
"""
from __future__ import annotations
from typing import Any, Dict, Literal, Optional, Union
from pydantic import BaseModel, Field
from pydantic import ValidationError
from abc import ABC, abstractmethod

from swarmstar.utils.misc.ids import generate_uuid, get_available_id, copy_under_new_swarm_id
from swarmstar.utils.database import MongoDBWrapper

db = MongoDBWrapper()

class SwarmOperation(BaseModel, ABC):
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
    def create(operation: SwarmOperation) -> None:
        db.create("swarm_operations", operation.id, operation.model_dump())

    @staticmethod
    def replace(operation: SwarmOperation) -> None:
        db.replace("swarm_operations", operation.id, operation.model_dump())

    @staticmethod
    def read(operation_id: str) -> SwarmOperation:
        operation = db.read("swarm_operations", operation_id)
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
        operation = SwarmOperation.read(operation_id)
        parts = operation.id.split("_", 1)
        operation.id = f"{new_swarm_id}_{parts[1]}"
        operation.create()

    @abstractmethod
    def get_field_updates_on_copy(self, new_swarm_id: str) -> Dict[str, Any]:
        pass


class BlockingOperation(SwarmOperation):
    operation_type: Literal["blocking"] = Field(default="blocking")
    node_id: str
    blocking_type: Literal[
        "instructor_completion",
        "openai_completion",
        "ask_questions",
    ]
    args: Dict[str, Any] = {}
    context: Dict[str, Any] = {}
    next_function_to_call: str
    
    def get_field_updates_on_copy(self, new_swarm_id: str) -> Dict[str, Any]:
        return {"node_id": copy_under_new_swarm_id(self.node_id, new_swarm_id)}

class SpawnOperation(SwarmOperation):
    operation_type: Literal["spawn"] = Field(default="spawn")
    action_id: str
    message: Union[str, Dict[str, Any]]
    context: Optional[Dict[str, Any]] = {}
    parent_id: Optional[str] = None
    node_id: Optional[str] = None

    def get_field_updates_on_copy(self, new_swarm_id: str) -> Dict[str, Any]:
        return {
            "action_id": copy_under_new_swarm_id(self.action_id, new_swarm_id),
            "parent_id": copy_under_new_swarm_id(self.parent_id, new_swarm_id),
            "node_id": copy_under_new_swarm_id(self.node_id, new_swarm_id)
        }

class ActionOperation(SwarmOperation):
    operation_type: Literal["action"] = Field(default="action")
    function_to_call: str
    node_id: str
    args: Dict[str, Any] = {}

    def get_field_updates_on_copy(self, new_swarm_id: str) -> Dict[str, Any]:
        return {"node_id": copy_under_new_swarm_id(self.node_id, new_swarm_id)}

class TerminationOperation(SwarmOperation):
    operation_type: Literal["terminate"] = Field(default="terminate")
    terminator_id: str
    node_id: str
    context: Optional[Dict[str, Any]] = None

    def get_field_updates_on_copy(self, new_swarm_id: str) -> Dict[str, Any]:
        return {
            "node_id": copy_under_new_swarm_id(self.node_id, new_swarm_id),
            "terminator_id": copy_under_new_swarm_id(self.terminator_id, new_swarm_id)
        }

class UserCommunicationOperation(SwarmOperation):
    operation_type: Literal["user_communication"] = Field(default="user_communication")
    node_id: str
    message: str
    context: Optional[Dict[str, Any]] = {}
    next_function_to_call: str

    def get_field_updates_on_copy(self, new_swarm_id: str) -> Dict[str, Any]:
        return {"node_id": copy_under_new_swarm_id(self.node_id, new_swarm_id)}