from swarmstar.models.base_node import BaseNode

class MetadataNode(BaseNode):
    is_folder: bool
    internal: bool
    description: str
