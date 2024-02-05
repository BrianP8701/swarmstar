'''
The swarm history is a record of all the events that have occurred in the swarm.
It stores all the information needed to reconstruct the state of the swarm at any
point in time.
'''

from typing import List
from pydantic import BaseModel, RootModel

from aga_swarm.swarm.types.swarm_lifecycle import SwarmNode, LifecycleCommand


class SwarmEvent(BaseModel):
    lifecycle_command: LifecycleCommand
    node: SwarmNode
    
class SwarmHistory(RootModel):
    root: List[SwarmEvent]
    
    def __iter__(self):
        return iter(self.root)
    
    def __getitem__(self, index: int) -> SwarmEvent:
        return self.root[index]
    
    def add_event(self, event: SwarmEvent):
        self.root.append(event)

