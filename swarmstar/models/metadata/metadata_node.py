from pydantic import Field

from swarmstar.models.base_node import BaseNode

class MetadataNode(BaseNode):
    is_folder: bool = Field(default=False)
    internal: bool = Field(default=True)
    description: str
