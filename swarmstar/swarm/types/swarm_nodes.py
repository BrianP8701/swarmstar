"""
The swarm consists of nodes. Each node is given a message 
and a preassigned action they must execute.
"""

from typing import Any, Dict, List, Optional

from pydantic import BaseModel
from typing_extensions import Literal


class SwarmNode(BaseModel):
    node_id: str
    parent_id: Optional[str] = None
    children_ids: List[str] = []
    action_id: str
    message: str
    alive: bool
    termination_policy: Literal[
        "simple",
        "parallel_review",
        "clone_with_questions_answered",
    ]
    developer_logs: List[Dict[str, Any]] = []
    journal: List[Dict[str, Any]] = []
    report: Optional[str] = None
