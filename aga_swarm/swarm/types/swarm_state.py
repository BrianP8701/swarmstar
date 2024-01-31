from typing import Dict
from pydantic import BaseModel

from aga_swarm.swarm.types.swarm_lifecycle import SwarmNode

class SwarmState(BaseModel):
    nodes: Dict[str, SwarmNode]
    
    def update_node(self, node_id: str, node: SwarmNode):
        self.nodes[node_id] = node
    