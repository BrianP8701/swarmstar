import json

from aga_swarm.swarm.types.swarm import SwarmID, SwarmState, SwarmHistory, Frame
from aga_swarm.swarm.types.metadata import ActionSpaceMetadata, MemorySpaceMetadata
from aga_swarm.swarm.types import SwarmNode, LifecycleCommand
from aga_swarm.actions.swarm.action_types.internal_default_swarm_action import internal_default_swarm_action

retrieve_file_action_id = 'aga_swarm/actions/data/file_operations/retrieve_file/retrieve_file.py'
upload_file_action_id = 'aga_swarm/actions/data/file_operations/upload_file/upload_file.py'

def get_swarm_state(swarm_id: SwarmID) -> SwarmState:
    state_bytes = internal_default_swarm_action(action_id=retrieve_file_action_id, 
        params={'file_path': swarm_id.state_path, "swarm_id": swarm_id})['data']
    state_str = state_bytes.decode('utf-8')
    state_dict = json.loads(state_str)
    return SwarmState.model_validate(state_dict)

def get_swarm_history(swarm_id: SwarmID) -> SwarmHistory:
    history_bytes = internal_default_swarm_action(action_id=retrieve_file_action_id, 
       params={'file_path': swarm_id.history_path, "swarm_id": swarm_id})['data']
    history_str = history_bytes.decode('utf-8')
    history_dict = json.loads(history_str)
    return SwarmHistory.model_validate(history_dict)

def get_action_space_metadata(swarm_id: SwarmID) -> ActionSpaceMetadata:
    action_space_bytes = internal_default_swarm_action(
        action_id=retrieve_file_action_id, 
        params={'file_path': swarm_id.action_space_metadata_path, "swarm_id": swarm_id}
    )['data']
    action_space_str = action_space_bytes.decode('utf-8')
    action_space_dict = json.loads(action_space_str)
    return ActionSpaceMetadata(action_space_dict)

def get_memory_space_metadata(swarm_id: SwarmID) -> MemorySpaceMetadata:
    memory_space_bytes = internal_default_swarm_action(
        action_id=retrieve_file_action_id, 
        params={'file_path': swarm_id.memory_space_metadata_path, "swarm_id": swarm_id}
    )['data']
    memory_space_str = memory_space_bytes.decode('utf-8')
    memory_space_dict = json.loads(memory_space_str)
    return MemorySpaceMetadata(memory_space_dict)

def get_action_type(swarm_id: SwarmID, action_id: str) -> str:
    action_space_metadata = get_action_space_metadata(swarm_id)
    return action_space_metadata.get(action_id)['type']

def get_action_name(swarm_id: SwarmID, action_id: str) -> str:
    action_space_metadata = get_action_space_metadata(swarm_id)
    return action_space_metadata.get(action_id)['name']

def upload_state(swarm_id: bytes, state: dict) -> dict:
    internal_default_swarm_action(action_id=upload_file_action_id, 
        params={'file_path': swarm_id.state_path, "data": state, "swarm_id":swarm_id})

def upload_history(swarm_id: bytes, history: SwarmHistory):
    internal_default_swarm_action(action_id=upload_file_action_id, 
        params={'file_path': swarm_id.history_path, "data": history, "swarm_id":swarm_id})

def update_state(swarm_id: SwarmID, node: SwarmNode):
    '''
        This must be a blocking operation to maintain consistency of the state
    '''
    current_state = get_swarm_state(swarm_id)
    current_state.update_node(node.node_id, node)
    upload_state(swarm_id, current_state.model_dump_json().encode('utf-8'))

def update_history(swarm_id: SwarmID, lifecycle_command: LifecycleCommand, node_id: str):
    '''
        This must be a blocking operation to maintain consistency of the state
    '''
    history = get_swarm_history(swarm_id)
    history.add_frame(Frame(
        node_id=node_id,
        lifecycle_command=lifecycle_command
    ))
    upload_history(swarm_id, history.model_dump_json().encode('utf-8'))