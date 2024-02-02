from pydantic import validate_call, BaseModel

from aga_swarm.utils.internal_swarm_utils import import_internal_python_action
from aga_swarm.swarm.types import SwarmConfig

class Input(BaseModel):
    swarm_config: SwarmConfig
    folder_path: str
    new_folder_path: str
    
class Output(BaseModel):
    success: bool
    error_message: str

@validate_call
def main(input: Input) -> Output:
    platform = input.swarm_config.platform.value
    main = import_internal_python_action(f'aga_swarm/actions/data/folder_operations/move_folder/{platform}_move_folder.py')
    return main(**{'folder_path': input.folder_path, 'new_folder_path': input.new_folder_path})
