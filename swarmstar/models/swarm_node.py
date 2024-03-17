"""
The swarm consists of nodes. Each node is given a message 
and a preassigned action they must execute.
"""

from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field
from typing_extensions import Literal

from swarmstar.utils.misc.generate_uuid import generate_uuid
from swarmstar.utils.data import MongoDBWrapper

db = MongoDBWrapper()

class SwarmNode(BaseModel):
    id: Optional[str] = Field(default_factory=lambda: generate_uuid("node"))
    name: str
    parent_id: Optional[str] = None
    children_ids: List[str] = []
    action_id: str
    message: str
    alive: bool = True
    termination_policy: Literal[
        "simple",
        "confirm_directive_completion",
        "custom_action_termination",
    ]
    developer_logs: List[Any] = []
    report: Optional[str] = None
    execution_memory: Optional[Dict[str, Any]] = {}
    context: Optional[Dict[str, Any]] = {}

    @staticmethod
    def save(node: 'SwarmNode') -> None:
        db.insert("swarm_nodes", node.id, node.model_dump())

    @staticmethod
    def get(node_id: str) -> 'SwarmNode':
        return SwarmNode.model_validate(db.get("swarm_nodes", node_id))

    @staticmethod
    def replace(node: 'SwarmNode') -> None:
        db.replace("swarm_nodes", node.id, node.model_dump())