from pydantic import validate_call

from aga_swarm.utils.internal_swarm_utils import import_internal_python_action
from aga_swarm.swarm.types.swarm import SwarmID

@validate_call
def main(swarm_id: SwarmID, file_path: str, data: bytes) -> dict:
    platform = swarm_id.platform.value
    main = import_internal_python_action(f'aga_swarm/actions/data/file_operations/upload_file/{platform}_upload_file.py')
    return main(**{'file_path': file_path, 'data': data})
