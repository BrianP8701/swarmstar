"""
Action metadata labels actions with descriptions.

Actions are predefined chains of logic, sprinkled with spots of ai
and human interaction to prouce intelligent behavior.

Every action can be found in swarmstar/actions

There is also going to be an action: "create_action". This will
allow for some form of self sufficiency.
"""
from typing import List, Optional, Type, TypeVar
from pydantic import Field
from enum import Enum
from typing_extensions import Literal
from importlib import import_module

from swarmstar.database import MongoDBWrapper
from swarmstar.models.metadata.metadata_node import MetadataNode
from swarmstar.utils.misc.get_next_available_id import get_available_id

db = MongoDBWrapper()
T = TypeVar('T', bound='ActionMetadata')

class ActionTypeEnum(Enum):
    PORTAL = "portal"
    BASIC = "basic"

class ActionMetadata(MetadataNode):
    id: str = Field(default_factory=get_available_id("action_metadata"))
    collection = "action_metadata"
    type = ActionTypeEnum

    @classmethod
    def get(cls: Type[T], action_id: str) -> T:
        """ Retrieve an action metadata node from the database and return an instance of the correct class. """
        # First, call the superclass (MetadataNode) get method to retrieve the node
        action_metadata_dict = super().get_node_dict(action_id)
        
        if action_metadata_dict["internal"]:
            if action_metadata_dict["is_folder"]:
                return InternalActionFolderMetadata(**action_metadata_dict)
            else:
                return InternalActionMetadata(**action_metadata_dict)
        else:
            if action_metadata_dict["is_folder"]:
                return ExternalActionFolderMetadata(**action_metadata_dict)
            else:
                return ExternalActionMetadata(**action_metadata_dict)

    @staticmethod
    def get_action_class(action_id: str):
        """ Returns an uninstantiated action class. """
        action_metadata_dict = ActionMetadata.get(action_id)
        if action_metadata_dict.is_folder:
            raise ValueError(f"You tried to get the action class of a folder {action_id}.")
        
        if action_metadata_dict.internal:
            internal_file_path = action_metadata_dict.internal_file_path
            action_class = getattr(import_module(internal_file_path), "Action")
            return action_class
        else:
            # TODO: Implement this when we have a better idea of how external actions will work.
            raise ValueError(f"External actions are not supported yet.")



class InternalActionMetadata(ActionMetadata):
    is_folder: Literal[False] = Field(default=False)
    internal: Literal[True] = Field(default=True)
    children_ids: Optional[List[str]] = Field(default=None)
    parent_id: str
    default_termination_policy: Literal["simple", "confirm_directive_completion"] = Field(default="simple")
    internal_file_path: str

class InternalActionFolderMetadata(ActionMetadata):
    is_folder: Literal[True] = Field(default=True)
    internal: Literal[True] = Field(default=True)

class ExternalActionMetadata(ActionMetadata):
    is_folder: Literal[False] = Field(default=False)
    internal: Literal[False] = Field(default=False)
    children_ids: Optional[List[str]] = Field(default=None)
    parent_id: str
    default_termination_policy: Literal["simple", "confirm_directive_completion"] = Field(default="simple")

class ExternalActionFolderMetadata(ActionMetadata):
    is_folder: Literal[True] = Field(default=True)
    internal: Literal[False] = Field(default=False)
