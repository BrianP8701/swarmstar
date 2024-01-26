from pydantic import validate_arguments

from aga_swarm.core.swarm.types import SwarmBlueprint, SwarmInstance, SwarmID
from aga_swarm.actions.swarm.action_types.internal_swarm_default_action import internal_swarm_default_action as execute

@validate_arguments
def swarm_lifecycle_executor(lifecycle_command: str, action: dict, swarm: SwarmID) -> dict:
    '''
    {
        "lifecycle_command": "spawn" or "terminate",
        "action" : {
            "type": "",
            "params": {}
        },
        "swarm": {
            "memory_space": {},
            "action_space": {},
            "nodes": {},
            "history": []
        }
    }
    '''
    if lifecycle_command is "spawn":
        return spawn_node(action, swarm)
    elif lifecycle_command is "terminate":
        return terminate_node(action, swarm)
    else:
        raise Exception(f"Invalid lifecycle command: {lifecycle_command}")

@validate_arguments
def spawn_node(action: dict, swarm: dict) -> dict:
    
    pass

@validate_arguments
def terminate_node(action: dict, swarm: dict) -> dict:
    pass

@validate_arguments
def action_executor(action: dict, swarm: dict) -> dict:
    return execute(action['type'], swarm, action['params'])

