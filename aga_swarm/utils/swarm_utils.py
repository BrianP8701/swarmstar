'''
    This module contains utility functions for interacting 
    with your swarm space outside of the package.
'''
import json
from importlib import import_module
from typing import Dict, Union
import pdb

from aga_swarm.swarm.types.swarm import SwarmID, SwarmState, SwarmHistory, Frame
from aga_swarm.swarm.types.metadata import *
from aga_swarm.swarm.types import SwarmNode, LifecycleCommand

def retrieve_file(swarm_id: SwarmID, file_path: str) -> bytes:
    retrieve_file_action_id = 'aga_swarm/actions/data/file_operations/retrieve_file/retrieve_file.py'
    main = _import_internal_python_action(retrieve_file_action_id)
    return main(swarm_id=swarm_id, file_path=file_path)['data']

def make_folder(swarm_id: SwarmID, folder_path: str) -> None:
    make_folder_action_id = 'aga_swarm/actions/data/folder_operations/make_folder/make_folder.py'
    main = _import_internal_python_action(make_folder_action_id)
    return main(swarm_id=swarm_id, folder_path=folder_path)

def upload_file(swarm_id: SwarmID, file_path: str, data: bytes) -> None:
    upload_file_action_id = 'aga_swarm/actions/data/file_operations/upload_file/upload_file.py'
    main = _import_internal_python_action(upload_file_action_id)
    return main(swarm_id=swarm_id, file_path=file_path, data=data)

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
    action_metadata = action_space_metadata.root[action_id]
    if action_metadata is None:
        raise ValueError(f"This action id {action_id} does not exist.")
    return action_metadata.type

def get_action_name(swarm_id: SwarmID, action_id: str) -> str:
    action_space_metadata = get_action_space_metadata(swarm_id)
    action_metadata = action_space_metadata.root[action_id]
    if action_metadata is None:
        raise ValueError(f"This action id {action_id} does not exist.")
    return action_metadata.name

def upload_state(swarm_id: SwarmID, state: SwarmState):
    upload_file(swarm_id, swarm_id.state_path, state.model_dump_json().encode('utf-8'))

def upload_history(swarm_id: SwarmID, history: SwarmHistory):
    upload_file(swarm_id, swarm_id.history_path, history.model_dump_json().encode('utf-8'))

def update_state(swarm_id: SwarmID, node: SwarmNode) -> None:
    '''
        This must be a blocking operation to maintain consistency of the state
    '''
    current_state = get_swarm_state(swarm_id)
    current_state.update_node(node.node_id, node)
    upload_state(swarm_id, current_state)

def update_history(swarm_id: SwarmID, lifecycle_command: LifecycleCommand, node_id: str) -> None:
    '''
        This must be a blocking operation to maintain consistency of the state
    '''
    history = get_swarm_history(swarm_id)
    history.add_frame(Frame(
        node_id=node_id,
        lifecycle_command=lifecycle_command
    ))
    upload_history(swarm_id, history)

def save_action_space_metadata(swarm_id: SwarmID, action_space_metadata: ActionSpaceMetadata):
    upload_file(swarm_id, swarm_id.action_space_metadata_path, action_space_metadata.model_dump_json().encode('utf-8'))
    
def _import_internal_python_action(module_name):
    module_name = module_name.replace('/', '.')
    module_name = module_name.replace('.py', '')
    module = import_module(module_name)
    main = getattr(module, 'main', None)  
    if main is None:
        raise AttributeError(f"No main function found in the script {module_name}")
    return main