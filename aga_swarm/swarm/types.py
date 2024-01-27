from pydantic import BaseModel
from typing import Dict, Any, Optional, List
from enum import Enum
    
class Configs(BaseModel):
    openai_key: str
    frontend_url: str
    
class SwarmID(BaseModel):
    instance_path: str
    root_path: str
    platform: str
    action_space_metadata_path: str
    memory_space_metadata_path: str
    stage_path: str
    state_path: str
    history_path: str
    configs: Configs

class LifecycleCommand(Enum):
    SPAWN= "spawn"
    TERMINATE = "terminate"

class NextActionCommand(BaseModel):
    action_id: str
    params: Dict[str, Any]
    
class SwarmCommand(BaseModel):
    lifecycle_command: LifecycleCommand
    action: NextActionCommand
    swarm_id: SwarmID
    
class NodeReport(BaseModel):
    success: bool
    message: str
    
class NodeOutput(BaseModel):
    swarm_commands: List[SwarmCommand]
    node_report: NodeReport