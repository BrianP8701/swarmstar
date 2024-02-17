from __future__ import annotations
from importlib import import_module
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from swarm_star.swarm.types import SwarmConfig, ActionMetadata

def execute_action(swarm: SwarmConfig, action_metadata: ActionMetadata, node_id: str, message: str):
    script_path = action_metadata.metadata['script_path']
    action_script = import_module(script_path)
    kwargs = {
        'swarm': swarm,
        'node_id': node_id,
        'message': message
    }
    return getattr(action_script, 'main')(**kwargs)
