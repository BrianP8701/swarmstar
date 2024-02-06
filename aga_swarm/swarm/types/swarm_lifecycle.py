'''
Here we define the smaller components that make up the swarm.

The lifecycle command describes the only 4 commands that an action
can send to the swarm. Spawn children nodes to take more actions,
execute itself, terminate itself if it completed its directive and 
needs no more children, or failure.

The swarm command and NodeIO are what nodes pass between each other.

The swarm node is the fundamental unit of the swarm.
'''

from enum import Enum
from pydantic import BaseModel
from typing import List, Optional, Dict, Any

from aga_swarm.swarm.types.swarm import Swarm

class LifecycleCommand(Enum):
    SPAWN= "spawn"
    EXECUTE = "execute"
    TERMINATE = "terminate"
    NODE_FAILURE = "node_failure"

class SwarmCommand(BaseModel):
    action_id: str
    directive: str
    
class NodeIO(BaseModel):
    lifecycle_command: LifecycleCommand
    swarm_commands: List[SwarmCommand]
    report: str
    
class BlockingOperation(BaseModel):
    node_id: str
    swarm: Swarm
    type: str
    args: Dict[str, Any]
    next_function_to_call: str
    
class SwarmNode(BaseModel):
    node_id: str
    parent_id: Optional[str] = None
    children_ids: List[str]
    swarm_command: SwarmCommand
    report: Optional[str] = None
    alive: bool
