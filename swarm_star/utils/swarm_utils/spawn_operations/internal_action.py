from importlib import import_module

from swarm_star.swarm.types import SwarmConfig, SwarmNode, SwarmState, ActionSpace, Action

def execute_action(swarm: SwarmConfig, node: SwarmNode, action_metadata: Action):
    action_id = node.action_id
    message = node.message
    action_space = ActionSpace(swarm=swarm)
    internal_action_path = action_metadata.metadata['internal_action_path']
    action_script = import_module(internal_action_path)
    kwargs = {
        'swarm': swarm,
        'node_id': node.node_id,
        'message': message
    }
    return getattr(action_script, 'main')(**kwargs)
