'''
The swarm state is a record of the current state of the swarm. It
simply stores a dictionary of all nodes. This state can be deconstructed
and reconstructed from the history.
'''
from __future__ import annotations
from pydantic import BaseModel
from typing import TYPE_CHECKING

from aga_swarm.utils.data.kv_operations.main import retrieve_swarm_space_kv_value, upload_swarm_space_kv_pair

if TYPE_CHECKING:
    from aga_swarm.swarm.types.swarm import Swarm
    from aga_swarm.swarm.types.swarm_lifecycle import SwarmNode

class SwarmState(BaseModel):
    swarm: Swarm
    
    def __getitem__(self, node_id: str) -> SwarmNode:
        node = SwarmNode.model_validate(retrieve_swarm_space_kv_value(self.swarm, 'swarm_state', node_id))
        return node
        
    def update_state(self, node: SwarmNode):
        upload_swarm_space_kv_pair(self.swarm, 'swarm_state', node.node_id, node.model_dump_json())
    