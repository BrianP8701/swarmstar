from pydantic import validate_call

from aga_swarm.actions.swarm.actions.action_types.internal_default_swarm_action import internal_default_swarm_action
from aga_swarm.swarm.types import SwarmID

@validate_call
def main(swarm_id: SwarmID, folder_path: str, new_folder_path: str) -> dict:
    platform = swarm_id.platform.value
    return internal_default_swarm_action(action_id=f'aga_swarm/actions/data/folder_operations/move_folder/{platform}_move_folder.py', 
        params={'folder_path': folder_path, 'new_folder_path': new_folder_path})
