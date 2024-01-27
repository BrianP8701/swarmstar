from pydantic import validate_arguments

from aga_swarm.actions.swarm.action_types.internal_swarm_default_action import internal_swarm_default_action as execute
from aga_swarm.swarm.types import SwarmID

@validate_arguments
def main(swarm_id: SwarmID, file_path: str, new_file_name: str) -> dict:
    platform = swarm_id.platform
    return execute(f'aga_swarm/actions/data/file_operations/rename_file/{platform}_rename_file.py', 
                   swarm_id, {'file_path': file_path, 'new_file_name': new_file_name})
