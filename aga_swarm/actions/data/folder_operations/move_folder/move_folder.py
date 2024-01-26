from pydantic import validate_arguments

from aga_swarm.actions.swarm.action_types.internal_python_script_call_main import internal_python_script_call_main as execute

@ validate_arguments
def main(swarm: dict, folder_path: str, new_folder_path: str) -> dict:
    platform = swarm['configs']['platform']
    return execute(f'aga_swarm/actions/data/folder_operations/move_folder/{platform}_move_folder.py', 
                   swarm, {'folder_path': folder_path, 'new_folder_path': new_folder_path})

