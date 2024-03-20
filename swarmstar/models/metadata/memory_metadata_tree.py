"""
The memory metadata tree allows the swarm to find answers to questions.
"""
from swarmstar.models.metadata.metadata_tree import MetadataTree

class MemoryMetadataTree(MetadataTree):
    collection = "memory_metadata"
