'''
The swarm config is a record of the configuration of the swarm. It
stores all the information about the environment in which the swarm 
is running. It also provides methods to interact with the swarm space.

The swarm config is a small data structure consisting only of strings,
and is passed around between every action. I made this so the swarm
could be decoupled and stateless. This is important for scalability.
'''

from enum import Enum
from pydantic import BaseModel
import json
from typing import Union

from aga_swarm.swarm.types.memory_metadata import MemorySpaceMetadata, MemoryMetadata, MemoryFolder
from aga_swarm.swarm.types.action_metadata import ActionSpaceMetadata, ActionMetadata, ActionFolder
from aga_swarm.swarm.types.swarm_state import SwarmState
from aga_swarm.swarm.types.swarm_history import SwarmHistory, SwarmEvent
from aga_swarm.swarm.types.swarm_lifecycle import LifecycleCommand, SwarmNode
from aga_swarm.swarm_utils.internal_package.get_resources import import_internal_python_action

class Configs(BaseModel):
    openai_key: str
    frontend_url: str
    azure_blob_storage_account_name: str
    azure_blob_storage_account_key: str
    azure_blob_storage_container_name: str
    azure_comsos_db_url: str
    azure_cosmos_db_key: str
    azure_cosmos_db_database_name: str
    azure_cosmos_db_container_name: str
    

class Platform(Enum):
    MAC = 'mac'
    AZURE = 'azure'

class Swarm(BaseModel):
    user_id: str
    swarm_id: str
    instance_path: str
    swarm_space_root_path: str
    platform: Platform
    action_space_metadata_path: str
    memory_space_metadata_path: str
    stage_path: str
    state_path: str
    history_path: str
    configs: Configs

    def get_action(self, action_id) -> Union[ActionSpaceMetadata, ActionFolder]:
        '''
        If mac 
        '''
        pass

    def get_memory(self, memory_id) -> Union[MemorySpaceMetadata, MemoryFolder]:
        pass    
    
    def get_node(self, node_id) -> SwarmNode:
        pass
    
    def get_state(self) -> SwarmState:
        pass
    
    def get_history(self) -> SwarmHistory:
        pass
    
    def update_state(self, node: SwarmNode) -> None:
        pass
    
    def update_history(self, lifecycle_command: LifecycleCommand, node_id: str) -> None:
        pass
    
    def get_action_space_metadata(self) -> ActionSpaceMetadata:
        pass

    def get_memory_space_metadata(self) -> MemorySpaceMetadata:
        pass
        

        
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
