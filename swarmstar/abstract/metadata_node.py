from typing import List, Optional, Dict, Any

from swarmstar.abstract.base_node import BaseNode
from swarmstar.utils.data import MongoDBWrapper

db = MongoDBWrapper()

class MetadataNode(BaseNode):
    is_folder: bool
    internal: bool
    descriptions: Optional[List[str]] = []          # Descriptive metadata in list form
    attributes: Optional[Dict[str, Any]] = {}       # Descriptive metadata in dict form
    type: str                               # Type of node/data (e.g. "portal", "file", "folder", "string")
    context: Optional[Dict[str, Any]] = {}  # Context for handlers specific to this node
