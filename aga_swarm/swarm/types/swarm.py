from pydantic import BaseModel
from enum import Enum
from typing import Dict, List, Any, Optional

class LifecycleCommand(Enum):
    SPAWN= "spawn"
    TERMINATE = "terminate"
    NODE_FAILURE = "node_failure"

class SwarmCommand(BaseModel):
    action_id: str
    params: Dict[str, Any]
    
class NodeOutput(BaseModel):
    lifecycle_command: LifecycleCommand
    swarm_commands: List[SwarmCommand]
    report: str
    
class SwarmNode(BaseModel):
    node_id: str
    parent_id: Optional[str] = None
    children_ids: List[str]
    swarm_command: SwarmCommand
    report: Optional[str] = None
    alive: bool

class Configs(BaseModel):
    openai_key: str
    frontend_url: str

class Platform(Enum):
    MAC = 'mac'
    WINDOWS = 'windows'
    LINUX = 'linux'
    AWS = 'aws'
    GCP = 'gcp'
    AZURE = 'azure'
    
class SwarmID(BaseModel):
    instance_path: str
    root_path: str
    platform: Platform
    action_space_metadata_path: str
    memory_space_metadata_path: str
    stage_path: str
    state_path: str
    history_path: str
    configs: Configs
    
class SwarmState(BaseModel):
    nodes: Dict[str, SwarmNode]
    
    def update_node(self, node_id: str, node_data: SwarmNode):
        self.nodes[node_id] = node_data
    
class Frame(BaseModel):
    lifecycle_command: LifecycleCommand
    node_id: str
    
class SwarmHistory(BaseModel):
    frames: List[Frame]
    
    def add_frame(self, frame: Frame):
        self.frames.append(frame)
