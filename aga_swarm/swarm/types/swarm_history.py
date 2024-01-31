from typing import List
from pydantic import BaseModel

from aga_swarm.swarm.types.swarm_lifecycle import LifecycleCommand

class Frame(BaseModel):
    lifecycle_command: LifecycleCommand
    node_id: str
    
class SwarmHistory(BaseModel):
    frames: List[Frame]
    
    def add_frame(self, frame: Frame):
        self.frames.append(frame)