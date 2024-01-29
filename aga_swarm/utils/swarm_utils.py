'''
    This module contains utility functions for interacting with the swarm
    space outside of the package.
'''

import json

from aga_swarm.swarm.types.swarm import SwarmID, SwarmState, SwarmHistory, Frame
from aga_swarm.swarm.types.metadata import ActionSpaceMetadata, MemorySpaceMetadata
from aga_swarm.swarm.types import SwarmNode, LifecycleCommand
from aga_swarm.actions.swarm.actions.action_types.internal_default_swarm_action import internal_default_swarm_action

retrieve_file_action_id = 'aga_swarm/actions/data/file_operations/retrieve_file/retrieve_file.py'
upload_file_action_id = 'aga_swarm/actions/data/file_operations/upload_file/upload_file.py'

def retrieve_file(swarm_id: SwarmID, file_path: str) -> bytes:
    output = internal_default_swarm_action(
        action_id=retrieve_file_action_id, 
        params={'file_path': file_path, "swarm_id": swarm_id}
    )
    if output['status'] == 'Success':
        return output['data']
    else:
        raise Exception(output['error_message'])

def upload_file(swarm_id: SwarmID, file_path: str, data: bytes):
    output = internal_default_swarm_action(
        action_id=upload_file_action_id, 
        params={'file_path': file_path, "data": data, "swarm_id": swarm_id}
    )
    if output['status'] == 'Success':
        return
    else:
        raise Exception(output['error_message'])

def get_swarm_state(swarm_id: SwarmID) -> SwarmState:
    state_bytes = retrieve_file(swarm_id, swarm_id.state_path)
    state_str = state_bytes.decode('utf-8')
    state_dict = json.loads(state_str)
    return SwarmState.model_validate(state_dict)

def get_swarm_history(swarm_id: SwarmID) -> SwarmHistory:
    history_bytes = retrieve_file(swarm_id, swarm_id.history_path)
    history_str = history_bytes.decode('utf-8')
    history_dict = json.loads(history_str)
    return SwarmHistory.model_validate(history_dict)

def get_action_space_metadata(swarm_id: SwarmID) -> ActionSpaceMetadata:
    action_space_bytes = retrieve_file(swarm_id, swarm_id.action_space_metadata_path)
    action_space_str = action_space_bytes.decode('utf-8')
    action_space_dict = json.loads(action_space_str)
    return ActionSpaceMetadata(action_space_dict)

def get_memory_space_metadata(swarm_id: SwarmID) -> MemorySpaceMetadata:
    memory_space_bytes = retrieve_file(swarm_id, swarm_id.memory_space_metadata_path)
    memory_space_str = memory_space_bytes.decode('utf-8')
    memory_space_dict = json.loads(memory_space_str)
    return MemorySpaceMetadata(memory_space_dict)

def get_action_type(swarm_id: SwarmID, action_id: str) -> str:
    action_space_metadata = get_action_space_metadata(swarm_id)
    action_metadata = action_space_metadata.get(action_id)
    if action_metadata is None:
        raise ValueError(f"This action id {action_id} does not exist.")
    return action_metadata['type']

def get_action_name(swarm_id: SwarmID, action_id: str) -> str:
    action_space_metadata = get_action_space_metadata(swarm_id)
    action_metadata = action_space_metadata.get(action_id)
    if action_metadata is None:
        raise ValueError(f"This action id {action_id} does not exist.")
    return action_metadata['name']

def upload_state(swarm_id: SwarmID, state: SwarmState):
    upload_file(swarm_id, swarm_id.state_path, state.model_dump_json().encode('utf-8'))

def upload_history(swarm_id: SwarmID, history: SwarmHistory):
    upload_file(swarm_id, swarm_id.history_path, history.model_dump_json().encode('utf-8'))

def update_state(swarm_id: SwarmID, node: SwarmNode):
    '''
        This must be a blocking operation to maintain consistency of the state
    '''
    current_state = get_swarm_state(swarm_id)
    current_state.update_node(node.node_id, node)
    upload_state(swarm_id, current_state)

def update_history(swarm_id: SwarmID, lifecycle_command: LifecycleCommand, node_id: str):
    '''
        This must be a blocking operation to maintain consistency of the state
    '''
    history = get_swarm_history(swarm_id)
    history.add_frame(Frame(
        node_id=node_id,
        lifecycle_command=lifecycle_command
    ))
    upload_history(swarm_id, history)