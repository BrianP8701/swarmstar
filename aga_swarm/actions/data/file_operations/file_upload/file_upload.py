from pydantic import validate_arguments

from aga_swarm.actions.swarm.action_types.internal_swarm_default_action import internal_swarm_default_action as execute

@ validate_arguments
def main(swarm: dict, file_path: str, data: bytes) -> dict:
    platform = swarm['configs']['platform']
    return execute(f'aga_swarm/actions/data/file_operations/file_upload/{platform}_file_upload.py', 
                   swarm, {'file_path': file_path, 'data': data})