from enum import Enum
from pydantic import BaseModel
from typing import Dict, List, Optional, Any

class LifecycleCommand(Enum):
    SPAWN= "spawn"
    EXECUTE = "execute"
    TERMINATE = "terminate"
    NODE_FAILURE = "node_failure"

class SwarmCommand(BaseModel):
    action_id: str
    params: Dict[str, Any]
    
class NodeOutput(BaseModel):
    lifecycle_command: LifecycleCommand
    swarm_commands: List[SwarmCommand]
    report: str
    
class SwarmNode(BaseModel):
    node_id: str
    parent_id: Optional[str] = None
    children_ids: List[str]
    swarm_command: SwarmCommand
    report: Optional[str] = None
    alive: bool