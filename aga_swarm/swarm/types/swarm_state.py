'''
The swarm state is a record of the current state of the swarm. It
simply stores a dictionary of all nodes. This state can be deconstructed
and reconstructed from the history.
'''

from typing import Dict
from pydantic import RootModel

from aga_swarm.swarm.types.swarm_lifecycle import SwarmNode

class SwarmState(RootModel):
    root: Dict[str, SwarmNode]
    
    def __iter__(self):
        return iter(self.root)
    
    def __getitem__(self, node_id: str) -> SwarmNode:
        node = self.root[node_id]
        if node is None:
            raise ValueError(f"This node id {node_id} does not exist.")
        return node
        
    def update_node(self, node_id: str, node: SwarmNode):
        self.root[node_id] = node
    