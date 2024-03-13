"""
The NodeEmbryo is what a node outputs to spawn children.

Nodes can perform 1 of 4 "SwarmOperations":
    - SpawnOperation
    - TerminationOperation
    - FailureOperation
    - BlockingOperation
    - UserCommunicationOperation
"""
from __future__ import annotations
from typing import Any, Dict, Literal, Optional, Union
from pydantic import BaseModel, Field

from swarmstar.utils.misc.generate_uuid import generate_uuid

class NodeEmbryo(BaseModel):
    action_id: str
    message: str


class SwarmOperation(BaseModel):
    id: str
    operation_type: Literal[
        "spawn",
        "terminate",
        "node_failure",
        "blocking",
        "user_communication",
        "action"
    ]

    @classmethod
    def model_validate(cls, data: Union[Dict[str, Any], 'SwarmOperation'], **kwargs) -> 'SwarmOperation':
        if isinstance(data, SwarmOperation):
            return data
        elif isinstance(data, dict):
            operation_type = data.get('operation_type')
            if operation_type == 'blocking':
                return BlockingOperation(**data)
            elif operation_type == 'spawn':
                return SpawnOperation(**data)
            elif operation_type == 'action':
                return ActionOperation(**data)
            elif operation_type == 'terminate':
                return TerminationOperation(**data)
            elif operation_type == 'node_failure':
                return FailureOperation(**data)
            elif operation_type == 'user_communication':
                return UserCommunicationOperation(**data)
        return super().model_validate(data, **kwargs)

class BlockingOperation(SwarmOperation):
    id: Optional[str] = Field(default_factory=lambda: generate_uuid('blocking_op'))
    operation_type: Literal["blocking"] = Field(default="blocking")
    node_id: str
    blocking_type: str
    args: Dict[str, Any] = {}
    context: Dict[str, Any] = {}
    next_function_to_call: str

class SpawnOperation(SwarmOperation):
    id: Optional[str] = Field(default_factory=lambda: generate_uuid('spawn_op'))
    operation_type: Literal["spawn"] = Field(default="spawn")
    node_embryo: NodeEmbryo
    parent_node_id: Optional[str] = None
    node_id: Optional[str] = None
    context: Optional[Dict[str, Any]] = None 

class ActionOperation(SwarmOperation):
    id: Optional[str] = Field(default_factory=lambda: generate_uuid('action_op'))
    operation_type: Literal["action"] = Field(default="action")
    function_to_call: str
    node_id: str
    args: Dict[str, Any] = {}

class TerminationOperation(SwarmOperation):
    id: Optional[str] = Field(default_factory=lambda: generate_uuid('termination_op'))
    operation_type: Literal["terminate"] = Field(default="terminate")
    terminator_node_id: str
    node_id: str
    context: Optional[Dict[str, Any]] = None

class FailureOperation(SwarmOperation):
    id: Optional[str] = Field(default_factory=lambda: generate_uuid('failure_op'))
    operation_type: Literal["node_failure"] = Field(default="node_failure")
    node_id: Optional[str] = None

class UserCommunicationOperation(SwarmOperation):
    id: Optional[str] = Field(default_factory=lambda: generate_uuid('user_comms_op'))
    operation_type: Literal["user_communication"] = Field(default="user_communication")
    node_id: str
    message: str
    context: Optional[Dict[str, Any]] = {}
    next_function_to_call: str
