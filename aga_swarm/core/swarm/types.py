from pydantic import BaseModel
from typing import Dict, Any

class SwarmBlueprint(BaseModel):
    swarm_blueprint: str
    action_space: Dict[str, Any]
    memory_space: Dict[str, Any]
    configs: Dict[str, Any]
    nodes: Dict[str, Any]
    history: list
    
class SwarmInstance(BaseModel):
    swarm_blueprint: str
    swarm_instance: str
    action_space: Dict[str, Any]
    memory_space: Dict[str, Any]
    configs: Dict[str, Any]
    nodes: Dict[str, Any]
    history: list
    
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