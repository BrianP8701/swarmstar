"""
The swarm consists of nodes. Each node is given a message 
and a preassigned action they must execute.
"""

from typing import Any, Dict, List, Optional

from typing_extensions import Literal

from swarmstar.utils.data import MongoDBWrapper
from swarmstar.abstract.base_node import BaseNode

db = MongoDBWrapper()

class SwarmNode(BaseNode):
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
    def get(node_id: str) -> 'SwarmNode':
        swarm_node_dict = super().get(node_id)
        return SwarmNode(**swarm_node_dict)

