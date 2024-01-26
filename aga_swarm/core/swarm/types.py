from pydantic import BaseModel
from typing import Dict, Any
    
class SwarmID(BaseModel):
    instance_path: str
    root_path: str
    platform: str
    action_space_metadata_path: str
    memory_space_metadata_path: str
    stage_path: str
    state_path: str
    history_path: str
    configs: Dict[str, Any]
    
