from pydantic import validate_arguments

from aga_swarm.actions.swarm.action_types.internal_default_swarm_action import internal_default_swarm_action
from aga_swarm.swarm.types.swarm import SwarmID

@validate_arguments
def main(swarm_id: SwarmID, file_path: str, data: bytes) -> dict:
    platform = swarm_id.platform
    return internal_default_swarm_action(action_id=f'aga_swarm/actions/data/file_operations/upload_file/{platform}_upload_file.py', 
        swarm_id=swarm_id, params={'file_path': file_path, 'data': data})

