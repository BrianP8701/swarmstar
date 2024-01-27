from aga_swarm.swarm.types.swarm import SwarmID, SwarmState, SwarmHistory, Frame
from aga_swarm.swarm.types.metadata import ActionSpaceMetadata, MemorySpaceMetadata
from aga_swarm.swarm.types import SwarmNode, LifecycleCommand
from aga_swarm.actions.swarm.action_types.internal_default_swarm_action import internal_default_swarm_action

retrieve_file_action_id = 'aga_swarm/actions/data/file_operations/retrieve_file/retrieve_file.py'
upload_file_action_id = 'aga_swarm/actions/data/file_operations/upload_file/upload_file.py'

def get_swarm_state(swarm_id: SwarmID) -> SwarmState:
    return internal_default_swarm_action(action_id=retrieve_file_action_id, swarm_id=swarm_id, 
        params={'file_path': swarm_id.state_path, "swarm_id": swarm_id})['data']

def get_swarm_history(swarm_id: SwarmID) -> SwarmHistory:
    return internal_default_swarm_action(action_id=retrieve_file_action_id, swarm_id=swarm_id, 
       params={'file_path': swarm_id.history_path, "swarm_id": swarm_id})['data']

def get_action_space_metadata(swarm_id: SwarmID) -> ActionSpaceMetadata:
    return internal_default_swarm_action(action_id=retrieve_file_action_id, swarm_id=swarm_id, 
        params={'file_path': swarm_id.action_space_metadata_path, "swarm_id": swarm_id})['data']

def get_memory_space_metadata(swarm_id: SwarmID) -> MemorySpaceMetadata:
    return internal_default_swarm_action(action_id=retrieve_file_action_id, swarm_id=swarm_id, 
        params={'file_path': swarm_id.memory_space_metadata_path, "swarm_id": swarm_id})['data']

def get_action_type(swarm_id: SwarmID, action_id: str) -> str:
    action_space_metadata = get_action_space_metadata(swarm_id)
    return action_space_metadata.get(action_id).type

def get_action_name(swarm_id: SwarmID, action_id: str) -> str:
    action_space_metadata = get_action_space_metadata(swarm_id)
    return action_space_metadata.get(action_id).name

def upload_state(swarm_id: SwarmID, state: dict) -> dict:
    return internal_default_swarm_action(action_id=upload_file_action_id, swarm_id=swarm_id, 
        params={'file_path': swarm_id.state_path, "data": state})['data']

def upload_history(swarm_id: SwarmID, history: SwarmHistory):
    return internal_default_swarm_action(action_id=upload_file_action_id, swarm_id=swarm_id, 
        params={'file_path': swarm_id.history_path, "data": history})['data']

def update_state(swarm_id: SwarmID, node: SwarmNode):
    '''
        This must be a blocking operation to maintain consistency of the state
    '''
    current_state = get_swarm_state(swarm_id)
    current_state.update_node(node.node_id, node.model_dump())
    upload_state(swarm_id, current_state)

def update_history(swarm_id: SwarmID, lifecycle_command: LifecycleCommand, node_id: str):
    '''
        This must be a blocking operation to maintain consistency of the state
    '''
    history = get_swarm_history(swarm_id)
    history.add_frame(Frame(
        node_id=node_id,
        lifecycle_command=lifecycle_command.model_dump()
    ))
    upload_history(swarm_id, history)