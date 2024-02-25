"""
The NodeEmbryo is what a node outputs to spawn children.

Nodes can perform 1 of 4 "SwarmOperations":
    - SpawnOperation
    - ExecuteOperation
    - TerminationOperation
    - FailureOperation
    - BlockingOperation
"""
from typing import Any, Dict, Literal, Optional

from pydantic import BaseModel, Field


class NodeEmbryo(BaseModel):
    action_id: str
    message: str


class SwarmOperation(BaseModel):
    operation_type: Literal["spawn", "terminate", "node_failure", "blocking"]
    node_id: str


class BlockingOperation(SwarmOperation):
    operation_type: Literal["blocking"] = Field(default="blocking")
    node_id: str
    blocking_type: str
    args: Dict[str, Any] = {}
    context: Dict[str, Any] = {}
    next_function_to_call: str

class SpawnOperation(SwarmOperation):
    operation_type: Literal["spawn"] = Field(default="spawn")
    node_embryo: NodeEmbryo
    termination_policy_change: Literal[
        "simple", "parallel_review", "clone_with_questions_answered"
    ] = None
    node_id: str = None


class TerminationOperation(SwarmOperation):
    operation_type: Literal["terminate"] = Field(default="terminate")
    node_id: str

class FailureOperation(SwarmOperation):
    operation_type: Literal["node_failure"] = Field(default="node_failure")
    node_id: Optional[str] = None
