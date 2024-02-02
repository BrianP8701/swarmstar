from typing import List
from pydantic import BaseModel

from aga_swarm.swarm.types.swarm_lifecycle import LifecycleCommand

class SwarmEvent(BaseModel):
    lifecycle_command: LifecycleCommand
    node_id: str
    
class SwarmHistory(BaseModel):
    frames: List[SwarmEvent]
    
    def add_frame(self, frame: SwarmEvent):
        self.frames.append(frame)