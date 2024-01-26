from pydantic import validate_arguments

from aga_swarm.actions.swarm.action_types.internal_python_script_call_main import internal_python_script_call_main as execute

@ validate_arguments
def main(swarm: dict, file_path: str) -> dict:
    platform = swarm['configs']['platform']
    return execute(f'aga_swarm/actions/data/file_operations/file_retrieval/{platform}_file_retrieval.py', 
                   swarm, {'file_path': file_path})

