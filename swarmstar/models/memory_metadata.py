"""
This module contains the nodes that make up the memory metadata tree.

The memory metadata tree allows the swarm to find answers to questions. It steps 
through the tree with a question and decides at each step which folder to navigate to
until it finds the answer.


"""
from typing import  List, Optional, TypeVar, Type, Dict, Any
from enum import Enum
from pydantic import Field
from typing_extensions import Literal

from swarmstar.database import MongoDBWrapper
from swarmstar.models.metadata_node import MetadataNode
from swarmstar.utils.misc.get_next_available_id import get_available_id

db = MongoDBWrapper()
T = TypeVar('T', bound='MemoryMetadata')

class MemoryTypeEnum(Enum):
    PORTAL = "portal"
    PYTHON_FILE = "python_file"
    PYTHON_PACKAGE = "python_package"
    PYTHON_CLASS = "python_class"
    PYTHON_FUNCTION = "python_function"
    GITHUB_LINK = "github_link"
    JSON_FILE = "json_file"
    CSV_FILE = "csv_file"
    MARKDOWN_FILE = "markdown_file"
    DOCUMENTATION_FOLDER = "documentation_folder"
    OTHER = "other"

class MemoryMetadata(MetadataNode):
    collection = "memory_metadata"
    id: str = Field(default_factory=get_available_id("memory_metadata"))
    type: MemoryTypeEnum # These define the type of the underlying data. Each type has tools to better navigate the data
    cache: Dict[str, Any] # If a node has been metafied, it will cache here
    up_to_date: bool # If the underlying data has changed, and the metadata is out of date

    @classmethod
    def get(cls: Type[T], action_id: str) -> T:
        """ Retrieve a memory metadata node from the database and return an instance of the correct class. """
        # First, call the superclass (MetadataNode) get method to retrieve the node
        memory_metadata_dict = super().get_node_dict(action_id)
        
        if memory_metadata_dict["internal"]:
            if memory_metadata_dict["is_folder"]:
                return InternalMemoryFolderMetadata(**memory_metadata_dict)
            else:
                return InternalMemoryMetadata(**memory_metadata_dict)
        else:
            if memory_metadata_dict["is_folder"]:
                return ExternalMemoryFolderMetadata(**memory_metadata_dict)
            else:
                return ExternalMemoryMetadata(**memory_metadata_dict)

class InternalMemoryMetadata(MemoryMetadata):
    is_folder: Literal[False] = Field(default=False)
    internal: Literal[True] = Field(default=True)
    children_ids: Optional[List[str]] = Field(default=None)
    parent_id: str

class InternalMemoryFolderMetadata(MemoryMetadata):
    is_folder: Literal[True] = Field(default=True)
    internal: Literal[True] = Field(default=True)
    children_ids: List[str]

class ExternalMemoryMetadata(MemoryMetadata):
    is_folder: Literal[False] = Field(default=False)
    internal: Literal[False] = Field(default=False)
    children_ids: Optional[List[str]] = Field(default=None)
    parent_id: str

class ExternalMemoryFolderMetadata(MemoryMetadata):
    is_folder: Literal[True] = Field(default=True)
    internal: Literal[False] = Field(default=False)
    children_ids: List[str]
