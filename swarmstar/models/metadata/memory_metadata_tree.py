"""
The memory metadata tree allows the swarm to find answers to questions.
"""
from typing import ClassVar

from swarmstar.models.metadata.metadata_tree import MetadataTree

class MemoryMetadataTree(MetadataTree):
    collection: ClassVar[str] = "memory_metadata"

    # @classmethod
    # def instantiate(cls, swarm_id: str) -> None:
    #     super()._instantiate(cls.collection, swarm_id)