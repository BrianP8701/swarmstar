"""
The action metadata tree allows the swarm to find actions to take.
"""
from typing import ClassVar

from swarmstar.models.metadata.metadata_tree import MetadataTree

class ActionMetadataTree(MetadataTree):
    collection: ClassVar[str] = "action_metadata"
