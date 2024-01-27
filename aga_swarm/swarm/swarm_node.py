from pydantic import BaseModel
from typing import Dict, Any, Optional, List
from aga_swarm.swarm.types import SwarmCommand

class SwarmNode(BaseModel):
    node_id: str
    action_id: str
    parent_id: Optional[str] = None
    children_ids: List[str]
    incoming_swarm_command: SwarmCommand
    report: dict
    alive: bool

    