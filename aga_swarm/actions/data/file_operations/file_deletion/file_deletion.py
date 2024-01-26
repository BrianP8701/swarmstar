from aga_swarm.actions.swarm.action_types.internal_python_script_call_main import internal_python_script_call_main as execute

def main(swarm: dict, file_path: str):
    platform = swarm['configs']['platform']
    return execute(f'aga_swarm/actions/data/file_operations/file_deletion/{platform}_file_deletion.py', 
                   swarm, {'file_path': file_path})

