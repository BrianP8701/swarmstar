from enum import Enum
from pydantic import BaseModel
import json

from aga_swarm.swarm.types.memory_metadata import MemorySpaceMetadata
from aga_swarm.swarm.types.action_metadata import ActionSpaceMetadata, ActionMetadata
from aga_swarm.swarm.types.swarm_state import SwarmState
from aga_swarm.swarm.types.swarm_history import SwarmHistory, SwarmEvent
from aga_swarm.swarm.types.swarm_lifecycle import LifecycleCommand, SwarmNode
from aga_swarm.swarm_utils.internal_package_utils.internal_swarm_utils import import_internal_python_action

class Configs(BaseModel):
    openai_key: str
    frontend_url: str

class Platform(Enum):
    MAC = 'mac'
    WINDOWS = 'windows'
    LINUX = 'linux'
    AWS = 'aws'
    GCP = 'gcp'
    AZURE = 'azure'

class SwarmConfig(BaseModel):
    instance_path: str
    swarm_space_root_path: str
    platform: Platform
    action_space_metadata_path: str
    memory_space_metadata_path: str
    stage_path: str
    state_path: str
    history_path: str
    configs: Configs

    def get_action_space_metadata(self) -> ActionSpaceMetadata:
        action_space_bytes = self._retrieve_file(self.action_space_metadata_path)
        action_space_str = action_space_bytes.decode('utf-8')
        action_space_dict = json.loads(action_space_str)
        return ActionSpaceMetadata.model_validate(action_space_dict)

    def get_memory_space_metadata(self) -> MemorySpaceMetadata:
        memory_space_bytes = self._retrieve_file(self.memory_space_metadata_path)
        memory_space_str = memory_space_bytes.decode('utf-8')
        memory_space_dict = json.loads(memory_space_str)
        return MemorySpaceMetadata.model_validate(memory_space_dict)

    def get_state(self) -> SwarmState:
        state_bytes = self._retrieve_file(self.state_path)
        state_str = state_bytes.decode('utf-8')
        state_dict = json.loads(state_str)
        return SwarmState.model_validate(state_dict)

    def get_history(self) -> SwarmHistory:
        history_bytes = self._retrieve_file(self.history_path)
        history_str = history_bytes.decode('utf-8')
        history_dict = json.loads(history_str)
        return SwarmHistory.model_validate(history_dict)
        
    def update_state(self, node: SwarmNode) -> None:
        '''
            This must be a blocking operation to maintain consistency of the state
        '''
        state = self.get_state()
        state.update_node(node.node_id, node)
        self._upload_file(self.state_path, state.model_dump_json().encode('utf-8'))

    def update_history(self, lifecycle_command: LifecycleCommand, node_id: str) -> None:
        '''
            This must be a blocking operation to maintain consistency of the state
        '''
        history = self.get_history()
        history.add_frame(SwarmEvent(
            node_id=node_id,
            lifecycle_command=lifecycle_command
        ))
        self._upload_file(self.history_path, history.model_dump_json().encode('utf-8'))
        
    def update_action_space_metadata(self, action_space_metadata: ActionSpaceMetadata) -> None:
        '''
            This must be a blocking operation to maintain consistency of the state
        '''
        self._upload_file(self.action_space_metadata_path, action_space_metadata.model_dump_json().encode('utf-8'))
        
    def delete_action_space_node(self, action_id: str) -> None:
        '''
        Delete an action space node and all it's children 
        from the action space and action space metadata.
        
        For now, this operates exclusively on the default
        swarm space. 

        Args:
            action_id (str): The id of the action to delete.
            action_space_metadata (dict): The action space metadata.
        '''
        action_space_metadata = self.get_action_space_metadata()
        action_space_metadata = self._delete_action_space_node_and_all_children(action_id, action_space_metadata)
        self.save_action_space_metadata(action_space_metadata)

    def add_action_space_node(action_id: str, action_space_metadata: ActionSpaceMetadata, action_metadata: ActionMetadata) -> None:
        '''
        Simply adds an action space node to the action space and 
        action space metadata.
        
        Args:
            action_id (str): The id of the action to add. This is the key in the action space metadata.
            action_space_metadata (dict): The action space metadata.
            action_metadata (ActionMetadata): The action metadata.
        '''
        action_space_metadata.root[action_id] = action_metadata
        parent_id = action_metadata.parent
        parent_metadata = action_space_metadata.root[parent_id]
        parent_metadata.children.append(action_id)


    '''
        Private Methods
    '''

    def _delete_action_space_node_and_all_children(self, action_id: str, action_space_metadata: ActionSpaceMetadata) -> None:
        '''
        Helper function for delete_action_space_node. Recursively
        deletes all children of the action space node and then the
        node itself. Returns the updated action space metadata.
        '''
        action_metadata = action_space_metadata.root[action_id]
        if action_metadata is None:
            raise ValueError(f"This action id {action_id} does not exist.")
            
        if action_metadata.type == 'folder':
            for child in list(action_metadata.children):
                self._delete_action_space_node_and_all_children(child, action_space_metadata)
            self._delete_action_node_helper(action_id, action_space_metadata)
        else:
            self._delete_action_node_helper(action_id, action_space_metadata)

    def _delete_action_node_helper(self, action_id: str, action_space_metadata: ActionSpaceMetadata):
        '''
        Delete an action from the action space and action space metadata.
        
        Only call this function after all its children have been deleted.
        '''
        action_metadata = action_space_metadata.root[action_id]
        if action_metadata.type == 'action':
            self._delete_file(action_metadata.script_path)
        elif action_metadata.type == 'folder':
            self._delete_folder(action_metadata.folder_path)
        
        parent_id = action_metadata.parent
        parent_metadata = action_space_metadata.root[parent_id]
        parent_metadata.children.remove(action_id)
        del action_space_metadata.root[action_id]
        
    def _upload_file(self, file_path: str, file_content: bytes):
        '''
        Uploads a file to the swarm space, on your platform.
        Write path relative to the root path.
        '''
        upload_file_action_id = 'aga_swarm/actions/data/file_operations/upload_file/upload_file.py'
        main = import_internal_python_action(upload_file_action_id)
        main(swarm_config=self, file_path=file_path, data=file_content)
        
    def _retrieve_file(self, file_path: str) -> bytes:
        '''
        Retrieves a file from the swarm space, on your platform.
        Write path relative to the root path.
        '''
        retrieve_file_action_id = 'aga_swarm/actions/data/file_operations/retrieve_file/retrieve_file.py'
        main = import_internal_python_action(retrieve_file_action_id)
        return main(swarm_config=self, file_path=file_path)['data']
        
    def _make_folder(self, folder_path: str) -> None:
        '''
        Makes a folder in the swarm space, on your platform.
        Write path relative to the root path.
        '''
        make_folder_action_id = 'aga_swarm/actions/data/folder_operations/make_folder/make_folder.py'
        main = import_internal_python_action(make_folder_action_id)
        return main(swarm_config=self, folder_path=folder_path)

    def _delete_file(self, file_path: str) -> None:
        '''
        Deletes a file in the swarm space, on your platform.
        Write path relative to the root path.
        '''
        delete_file_action_id = 'aga_swarm/actions/data/file_operations/delete_file/delete_file.py'
        main = import_internal_python_action(delete_file_action_id)
        return main(swarm_config=self, file_path=file_path)
    
    def _delete_foler(self, folder_path: str) -> None:
        '''
        Deletes a folder in the swarm space, on your platform.
        Write path relative to the root path.
        '''
        delete_folder_action_id = 'aga_swarm/actions/data/folder_operations/delete_folder/delete_folder.py'
        main = import_internal_python_action(delete_folder_action_id)
        return main(swarm_config=self, folder_path=folder_path)