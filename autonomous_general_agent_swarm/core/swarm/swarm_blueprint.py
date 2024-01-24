from pydantic import BaseModel, Field
import importlib
from typing import Callable, BinaryIO

from core.swarm.configuration_utils import get_default_action_tree, get_default_memory_tree

class Swarm(BaseModel):
    '''
    Create and configure your swarm with your environment and data.
    
    Parameters:
        - swarm_name (str)
        - openai_key (str)
        - frontend_url (str): The URL for the frontend interface of the swarm.
        - file_storage_upload (str): The string representation of the method used for uploading files to storage.
        - file_storage_retrieval (str): The string representation of the method used for retrieving files from storage.
        - make_folder (str): The string representation of the method used for creating a folder at a given path.
        - delete_folder (str): The string representation of the method used for deleting a folder at a given path.
    '''
    swarm_name: str = Field(...)
    openai_key: str = Field(...)
    frontend_url: str = Field(...)
    file_storage_upload: str = Field(...)
    file_storage_retrieval: str = Field(...)
    make_folder: str = Field(...)
    delete_folder: str = Field(...)

    def __init__(self, swarm_name: str, openai_key: str, frontend_url: str, 
                 file_storage_upload: str, 
                 file_storage_retrieval: str,
                 make_folder: str,
                 delete_folder: str):
        # Convert string representations to callable functions and assign to self
        for method_name in ['file_storage_upload', 'file_storage_retrieval', 'make_folder', 'delete_folder']:
            module_name, func_name = locals()[method_name].rsplit('.', 1)
            module = importlib.import_module(module_name)
            setattr(self, method_name, getattr(module, func_name))

        super().__init__(swarm_name=swarm_name, openai_key=openai_key, 
                         frontend_url=frontend_url, file_storage_upload=file_storage_upload, 
                         file_storage_retrieval=file_storage_retrieval,
                         make_folder=make_folder, delete_folder=delete_folder)
    
    def _configure(self):
        # Create a folder for this swarm blueprint at the given path.
        self.root_path = f'{self.swarm_name}/swarm_blueprint'
        self.make_folder(self.root_path)
        # Copy the default action and memory space into the swarm blueprint folder.
        self.action_space = get_default_action_tree()
        self.memory_space = get_default_memory_tree()
        # Configure the swarm with the provided configuration.
        pass

