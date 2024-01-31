from pydantic import validate_call

from aga_swarm.utils.internal_swarm_utils import import_internal_python_action
from aga_swarm.swarm.types import SwarmSpace

@validate_call
def main(swarm_space: SwarmSpace, folder_path: str, new_folder_path: str) -> dict:
    platform = swarm_space.platform.value
    main = import_internal_python_action(f'aga_swarm/actions/data/folder_operations/rename_folder/{platform}_rename_folder.py')
    return main(**{'folder_path': folder_path, 'new_folder_name': new_folder_path})
