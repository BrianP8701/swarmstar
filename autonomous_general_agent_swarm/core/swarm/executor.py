from pydantic import validate_arguments

@validate_arguments
def swarm_official_executor(lifecycle_command: str, action: dict, swarm: dict) -> dict:
    '''
    {
        "lifecycle_command": "spawn" or "terminate",
        "action" : {
            "id": "",
            "args": {}
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
