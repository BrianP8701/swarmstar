from pydantic import validate_arguments

from aga_swarm.actions.swarm.action_types.internal_default_swarm_action import internal_default_swarm_action
from aga_swarm.swarm.types import SwarmID

@validate_arguments
def main(swarm_id: SwarmID, file_path: str) -> dict:
    platform = swarm_id.platform
    return internal_default_swarm_action(action_id=f'aga_swarm/actions/data/file_operations/retrieve_file/{platform}_retrieve_file.py', 
        swarm_id=swarm_id, params={'file_path': file_path})

