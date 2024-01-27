from pydantic import validate_arguments

from aga_swarm.swarm.types import SwarmID
from aga_swarm.actions.swarm.action_types.internal_swarm_default_action import internal_swarm_default_action as execute

retrieve_file_action_id = 'aga_swarm/actions/data/file_operations/retrieve_file/retrieve_file.py'

@validate_arguments
def get_swarm_state(swarm_id: SwarmID) -> dict:
    return execute(retrieve_file_action_id, swarm_id, 
        {'file_path': swarm_id.state_path, "swarm_id": swarm_id})['data']

@validate_arguments
def get_swarm_history(swarm_id: SwarmID) -> list:
    return execute(retrieve_file_action_id, swarm_id, 
        {'file_path': swarm_id.history_path, "swarm_id": swarm_id})['data']
    
@validate_arguments
def get_action_space_metadata(swarm_id: SwarmID) -> dict:
    return execute(retrieve_file_action_id, swarm_id, 
        {'file_path': swarm_id.action_space_metadata_path, "swarm_id": swarm_id})['data']

@validate_arguments
def get_memory_space_metadata(swarm_id: SwarmID) -> dict:
    return execute(retrieve_file_action_id, swarm_id, 
        {'file_path': swarm_id.memory_space_metadata_path, "swarm_id": swarm_id})['data']

@validate_arguments
def get_action_type(swarm_id: SwarmID, action_id: str) -> str:
    action_space_metadata = get_action_space_metadata(swarm_id)
    return action_space_metadata[action_id]['type']