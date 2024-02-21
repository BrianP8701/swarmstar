from importlib import import_module
from typing import Union, List

from swarmstar.swarm.types import SwarmConfig, SwarmNode, Action, SwarmOperation

def execute_action(swarm: SwarmConfig, node: SwarmNode, action_metadata: Action) -> Union[SwarmOperation, List[SwarmOperation]]:
    message = node.message
    internal_action_path = action_metadata.internal_action_path
    action_script = import_module(internal_action_path)
    kwargs = {
        'swarm': swarm,
        'node_id': node.node_id,
        'message': message
    }
    return getattr(action_script, 'main')(**kwargs)
