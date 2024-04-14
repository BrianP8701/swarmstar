from pydantic import Field
from typing import Optional

from swarmstar.models.base_node import BaseNode

class MetadataNode(BaseNode):
    """
    This is the base class for the nodes that make up the action and memory metadata trees. Metadata trees are data structures that an LLM can navigate.
    """
    is_folder: Optional[bool] = Field(default=None)
    internal: Optional[bool] = Field(default=None)
    portal: Optional[bool] = Field(default=None)
    description: str
