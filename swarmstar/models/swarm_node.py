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
    execution_memory: Optional[Dict[str, Any]] = None
    context: Optional[Dict[str, Any]] = None

    @staticmethod
    def insert_swarm_node(node: 'SwarmNode') -> None:
        db.insert("swarm_nodes", node.id, node.model_dump())

    @staticmethod
    def update_swarm_node(node: 'SwarmNode') -> None:
        db.update("swarm_nodes", node.id, node.model_dump())

    @staticmethod
    def get_swarm_node(node_id: str) -> 'SwarmNode':
        return SwarmNode.model_validate(db.get("swarm_nodes", node_id))
