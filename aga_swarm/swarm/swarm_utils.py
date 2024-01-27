from pydantic import validate_arguments

from aga_swarm.swarm.types import SwarmID, SwarmNode, SwarmState, SwarmHistory, SwarmCommand, LifecycleCommand, Frame
from aga_swarm.actions.swarm.action_types.internal_swarm_default_action import internal_swarm_default_action as execute

retrieve_file_action_id = 'aga_swarm/actions/data/file_operations/retrieve_file/retrieve_file.py'
upload_file_action_id = 'aga_swarm/actions/data/file_operations/upload_file/upload_file.py'

@validate_arguments
def get_swarm_state(swarm_id: SwarmID) -> SwarmState:
    return execute(retrieve_file_action_id, swarm_id, 
        {'file_path': swarm_id.state_path, "swarm_id": swarm_id})['data']

@validate_arguments
def get_swarm_history(swarm_id: SwarmID) -> SwarmHistory:
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

@validate_arguments
def get_action_name(swarm_id: SwarmID, action_id: str) -> str:
    action_space_metadata = get_action_space_metadata(swarm_id)
    return action_space_metadata[action_id]['name']

@validate_arguments
def upload_state(swarm_id: SwarmID, state: dict) -> dict:
    return execute(upload_file_action_id, swarm_id, 
        {'file_path': swarm_id.state_path, "data": state})['data']

@validate_arguments
def upload_history(swarm_id: SwarmID, history: SwarmHistory):
    return execute(upload_file_action_id, swarm_id, 
        {'file_path': swarm_id.history_path, "data": history})['data']

@validate_arguments
def update_state(swarm_id: SwarmID, node: SwarmNode):
    '''
        This must be a blocking operation to maintain consistency of the state
    '''
    current_state = get_swarm_state(swarm_id)
    current_state[node.node_id] = node.model_dump()
    upload_state(swarm_id, current_state)
    
@validate_arguments
def update_history(swarm_id: SwarmID, lifecycle_command: LifecycleCommand, node_id: str):
    '''
        This must be a blocking operation to maintain consistency of the state
    '''
    history = get_swarm_history(swarm_id)
    history.frames.append(Frame(
        node_id=node_id,
        lifecycle_command=lifecycle_command.model_dump()
    ))
    upload_history(swarm_id, history)