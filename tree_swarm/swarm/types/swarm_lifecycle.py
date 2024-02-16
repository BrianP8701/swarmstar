'''
Here we define the smaller components that make up the swarm.

The lifecycle command describes the only 4 commands that an action
can send to the swarm. Spawn children nodes to take more actions,
execute itself, terminate itself if it completed its directive and 
needs no more children, or failure.

The swarm command and NodeIO are what nodes pass between each other.

The swarm node is the fundamental unit of the swarm.
'''

from pydantic import BaseModel
from typing import List, Dict, Any
from typing_extensions import Literal

class SwarmNode(BaseModel):
    node_id: str
    parent_id: str
    children_ids: List[str]
    action_id: str
    message: str
    report: str
    alive: bool
    termination_policy: Literal['terminate', 'managerial_review', 'retry_with_comms', 'consolidate_report']

class NodeEmbryo(BaseModel):
    action_id: str
    message: str

class SwarmOperation(BaseModel):
    lifecycle_command: Literal['spawn', 'terminate', 'node_failure', 'blocking_operation']

class BlockingOperation(SwarmOperation):
    lifecycle_command: Literal['blocking_operation']
    node_id: str 
    type: str  
    args: Dict[str, Any] 
    next_function_to_call: str 

class SpawnOperation(SwarmOperation):
    lifecycle_command: Literal['spawn']
    swarm_commands: List[NodeEmbryo]
    report: str

class TerminateOperation(SwarmOperation):
    lifecycle_command: Literal['terminate']
    report: str
    
class FailureOperation(SwarmOperation):
    lifecycle_command: Literal['node_failure']
    report: str
    