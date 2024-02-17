'''
The swarm consists of nodes. Each node is given a message and a preassigned action they must execute.

The NodeEmbryo is what a node outputs to spawn children.

Nodes can perform 1 of 4 "SwarmOperations":
    - SpawnOperation
    - ExecuteOperation
    - TerminateOperation
    - FailureOperation
    - BlockingOperation
'''

from pydantic import BaseModel
from typing import List, Dict, Any
from typing_extensions import Literal

class SwarmNode(BaseModel):
    node_id: str
    parent_id: str = ''
    children_ids: List[str]
    action_id: str
    message: str
    report: str = ''
    alive: bool
    termination_policy: Literal[
        'simple',
        'append_reports' 
        'parallel_review', 
        'clone_self_with_reports',
        'consolidate_reports'
    ] 

class NodeEmbryo(BaseModel):
    action_id: str
    message: str

class SwarmOperation(BaseModel):
    operation_type: Literal['spawn', 'terminate', 'node_failure', 'blocking', 'execute']
    node_id: str

class ExecuteOperation(SwarmOperation):
    operation_type: Literal['execute']
    node: SwarmNode

class BlockingOperation(SwarmOperation):
    operation_type: Literal['blocking']
    node_id: str 
    blocking_type: str  
    args: Dict[str, Any] = {}
    context: Dict[str, Any] = {}
    next_function_to_call: str 

class SpawnOperation(SwarmOperation):
    operation_type: Literal['spawn']
    node_id: str = ''
    node_embryos: List[NodeEmbryo]
    report: str = ''

class TerminateOperation(SwarmOperation):
    operation_type: Literal['terminate']
    node_id: str
    report: str
    
class FailureOperation(SwarmOperation):
    operation_type: Literal['node_failure']
    node_id: str
    report: str
    