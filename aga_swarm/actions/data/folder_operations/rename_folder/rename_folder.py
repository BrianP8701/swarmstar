from pydantic import validate_arguments

from aga_swarm.actions.swarm.action_types.internal_default_swarm_action import internal_default_swarm_action
from aga_swarm.swarm.types import SwarmID

@validate_arguments
def main(swarm_id: SwarmID, folder_path: str, new_folder_path: str) -> dict:
    platform = swarm_id.platform.value
    return internal_default_swarm_action(action_id=f'aga_swarm/actions/data/folder_operations/rename_folder/{platform}_rename_folder.py', 
        parmas={'folder_path': folder_path, 'new_folder_name': new_folder_path})
