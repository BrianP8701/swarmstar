'''
The swarm history is a record of all the events that have occurred in the swarm.
It stores all the information needed to reconstruct the state of the swarm at any
point in time.
'''
from pydantic import BaseModel

from swarmstar.utils.data.kv_operations.main import get_kv, add_kv
from swarmstar.swarm.types.swarm_config import SwarmConfig
from swarmstar.swarm.types.swarm_operations import SwarmOperation
    
    
class SwarmHistory(BaseModel):
    swarm: SwarmConfig

    def __getitem__(self, frame: int) -> SwarmOperation:
        return SwarmOperation.model_validate(get_kv(self.swarm, 'swarm_history', frame))
    
    def add_event(self, operation: SwarmOperation):
        current_frame = get_kv(self.swarm, 'swarm_history', 'current_frame')['frame']
        add_kv(self.swarm, 'swarm_history', current_frame, operation.model_dump())
        add_kv(self.swarm, 'swarm_history', 'current_frame', {'frame': current_frame + 1})
