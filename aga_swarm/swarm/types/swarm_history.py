'''
The swarm history is a record of all the events that have occurred in the swarm.
It stores all the information needed to reconstruct the state of the swarm at any
point in time.
'''

from typing import List
from pydantic import BaseModel, RootModel

from aga_swarm.swarm.types.swarm_lifecycle import SwarmNode, LifecycleCommand
from aga_swarm.swarm.types.swarm import Swarm
from aga_swarm.utils.data.kv_operations.main import retrieve_swarm_space_kv_value, upload_swarm_space_kv_pair

class SwarmEvent(BaseModel):
    lifecycle_command: LifecycleCommand
    node: SwarmNode
    
class SwarmHistory(RootModel):
    swarm: Swarm

    def __getitem__(self, frame: int) -> SwarmEvent:
        return SwarmEvent.model_validate(retrieve_swarm_space_kv_value(self.swarm, 'swarm_history', frame))
    
    def add_event(self, lifecycle_command: LifecycleCommand, node: SwarmNode):
        current_frame = retrieve_swarm_space_kv_value(self.swarm, 'swarm_history', 'current_frame')
        upload_swarm_space_kv_pair(self.swarm, 'swarm_history', current_frame, SwarmEvent(lifecycle_command=lifecycle_command, node=node).model_dump_json())
        upload_swarm_space_kv_pair(self.swarm, 'swarm_history', 'current_frame', current_frame + 1)

