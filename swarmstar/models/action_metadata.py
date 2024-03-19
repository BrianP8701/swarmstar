from typing import List, Optional, Type, TypeVar
from pydantic import Field
from typing_extensions import Literal

from swarmstar.utils.data import MongoDBWrapper
from swarmstar.abstract.metadata_node import MetadataNode

db = MongoDBWrapper()

T = TypeVar('T', bound='ActionMetadata')


class ActionMetadata(MetadataNode):
    type: Literal[
        "internal_folder",
        "internal_action",
    ]


    @classmethod
    def get(cls: Type[T], action_id: str) -> T:
        # First, call the superclass (MetadataNode) get method to retrieve the node
        action_metadata_dict = super().get(action_id)
        
        # Define a mapping from type to the corresponding class
        type_mapping = {
            "internal_action": InternalAction,
            "internal_folder": InternalFolder,
            # Add other types as necessary
        }
        
        # Use the type attribute to determine the correct class to instantiate
        action_type = action_metadata_dict["type"]
        if action_type in type_mapping:
            # Return an instance of the correct type, passing the action_metadata as initialization arguments
            return type_mapping[action_type](**action_metadata_dict)
        else:
            # If the type is not in the mapping, you might want to handle this case (e.g., raise an error)
            raise ValueError(f"Unknown action type: {action_type}")


class InternalAction(ActionMetadata):
    type: Literal["internal_action"] = Field(default="internal_action")
    name: str
    description: str
    children_ids: Optional[List[str]] = Field(default=None)
    parent: str
    termination_policy: Literal["simple", "confirm_directive_completion", "clone_with_questions_answered"] = Field(default="simple")
    internal_action_path: str


class InternalFolder(ActionMetadata):
    type: Literal["internal_folder"] = Field(default="internal_folder")
    name: str
    description: str
    children_ids: List[str]
    parent: str = None
    internal_folder_path: str
