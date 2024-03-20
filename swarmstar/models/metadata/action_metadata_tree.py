"""
The action metadata tree allows the swarm to find actions to take.
"""
from swarmstar.models.metadata.metadata_tree import MetadataTree

class ActionMetadataTree(MetadataTree):
    collection = "action_metadata"