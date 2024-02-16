from __future__ import annotations
from importlib import import_module
from typing import Dict, Any, TYPE_CHECKING

if TYPE_CHECKING:
    from tree_swarm.swarm.types import Swarm, ActionMetadata

def execute_action(swarm: Swarm, action_metadata: ActionMetadata, node_id: str, message: str):
    script_path = action_metadata.execution_metadata['script_path']
    action_script = import_module(script_path)
    return getattr(action_script, 'main')(swarm=swarm, node_id=node_id, message=message)
