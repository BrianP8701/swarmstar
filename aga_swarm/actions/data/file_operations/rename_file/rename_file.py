from pydantic import validate_call

from aga_swarm.utils.internal_swarm_utils import import_internal_python_action
from aga_swarm.swarm.types import SwarmID

@validate_call
def main(swarm_id: SwarmID, file_path: str, new_file_name: str) -> dict:
    platform = swarm_id.platform.value
    main = import_internal_python_action(f'aga_swarm/actions/data/file_operations/rename_file/{platform}_rename_file.py')
    return main(**{'file_path': file_path, 'new_file_name': new_file_name})
