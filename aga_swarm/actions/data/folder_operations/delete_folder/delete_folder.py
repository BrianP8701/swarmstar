from pydantic import validate_call

from aga_swarm.utils.internal_swarm_utils import import_internal_python_action
from aga_swarm.swarm.types import SwarmID

@validate_call
def main(swarm_id: SwarmID, folder_path: str) -> dict:
    platform = swarm_id.platform.value
    main = import_internal_python_action(f'aga_swarm/actions/data/folder_operations/delete_folder/{platform}_delete_folder.py')
    return main(**{'folder_path': folder_path})
