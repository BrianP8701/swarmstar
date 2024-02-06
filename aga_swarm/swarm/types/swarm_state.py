'''
The swarm state is a record of the current state of the swarm. It
simply stores a dictionary of all nodes. This state can be deconstructed
and reconstructed from the history.
'''

from typing import Dict
from pydantic import RootModel
import json

from aga_swarm.swarm.types.swarm_lifecycle import SwarmNode
from aga_swarm.swarm.types.swarm import Swarm
from aga_swarm.utils.data.kv_operations.main import retrieve_swarm_space_kv_value, upload_swarm_space_kv_pair

class SwarmState(RootModel):
    swarm: Swarm
    
    def __getitem__(self, node_id: str) -> SwarmNode:
        node = SwarmNode.model_validate(retrieve_swarm_space_kv_value(self.swarm, 'swarm_state', node_id))
        return node
        
    def update_node(self, node: SwarmNode):
        upload_swarm_space_kv_pair(self.swarm, 'swarm_state', node.node_id, node.model_dump_json())
    