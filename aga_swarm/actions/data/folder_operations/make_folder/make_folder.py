from pydantic import validate_arguments

from aga_swarm.actions.swarm.action_types.internal_swarm_default_action import internal_swarm_default_action as execute
from aga_swarm.swarm.types import SwarmID

@validate_arguments
def main(swarm_id: SwarmID, folder_path: str) -> dict:
    platform = swarm_id.platform
    return execute(f'aga_swarm/actions/data/folder_operations/make_folder/{platform}_make_folder.py', 
                   swarm_id, {'folder_path': folder_path})