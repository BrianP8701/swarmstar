from pydantic import validate_call, BaseModel

from aga_swarm.utils.internal_swarm_utils import import_internal_python_action
from aga_swarm.swarm.types import SwarmConfig

class Input(BaseModel):
    swarm_config: SwarmConfig
    file_path: str
    new_file_name: str

class Output(BaseModel):
    success: bool
    error_message: str

@validate_call
def main(input: Input) -> Output:
    platform = input.swarm_config.platform.value
    main = import_internal_python_action(f'aga_swarm/actions/data/file_operations/rename_file/{platform}_rename_file.py')
    return main(**{'file_path': input.file_path, 'new_file_name': input.new_file_name})
