from pydantic import validate_call

from aga_swarm.utils.internal_swarm_utils import import_internal_python_action
from aga_swarm.swarm.types import SwarmSpace

@validate_call
def main(swarm_space: SwarmSpace, file_path: str) -> dict:
    platform = swarm_space.platform.value
    main = import_internal_python_action(f'aga_swarm/actions/data/file_operations/retrieve_file/{platform}_retrieve_file.py')
    return main(**{'file_path': file_path})

