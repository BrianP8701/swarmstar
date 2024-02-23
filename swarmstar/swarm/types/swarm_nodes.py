'''
The swarm consists of nodes. Each node is given a message and a preassigned action they must execute.
'''

from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
from typing_extensions import Literal

class SwarmNode(BaseModel):
    node_id: str
    parent_id: Optional[str] = None
    children_ids: List[str] = []
    action_id: str
    message: str
    report: Optional[str] = None
    alive: bool
    journal: List[Dict[str, Any]] = []
    termination_policy: Literal[
        'simple',
        'parallel_review', 
        'clone_with_reports'
    ] 
