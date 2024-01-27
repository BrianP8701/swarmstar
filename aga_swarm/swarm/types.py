from pydantic import BaseModel
from typing import Dict, Any, Optional, List
from enum import Enum
    
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

class LifecycleCommand(Enum):
    SPAWN= "spawn"
    TERMINATE = "terminate"

class SwarmCommand(BaseModel):
    action_id: str
    params: Dict[str, Any]
    
class NodeStatus(Enum):
    SUCCESS = "success"
    FAILED = "failed"
    
class NodeReport(BaseModel):
    status: NodeStatus
    message: str
    
class NodeOutput(BaseModel):
    lifecycle_command: LifecycleCommand
    swarm_commands: List[SwarmCommand]
    node_report: NodeReport
    
class SwarmNode(BaseModel):
    node_id: str
    action_id: str
    parent_id: Optional[str] = None
    children_ids: List[str]
    incoming_swarm_command: SwarmCommand
    report: NodeReport
    alive: bool

class SwarmState(BaseModel):
    nodes: Dict[str, SwarmNode]
    
class Frame(BaseModel):
    lifecycle_command: LifecycleCommand
    node_id: str
    
class SwarmHistory(BaseModel):
    frames: List[Frame]


