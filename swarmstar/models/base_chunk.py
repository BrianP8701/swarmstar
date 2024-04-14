"""
A chunk is data. It can be anything from a string, repository or image.

Every memory metadata node corresponds to a chunk of data. 
"""
from abc import ABC, abstractmethod, abstractclassmethod
from pydantic import BaseModel, ConfigDict
from typing import List, Optional, Type, TypeVar

from swarmstar.models.metadata.memory_types import MemoryType

class BaseChunk(ABC, BaseModel):
    type: MemoryType
    
    config: ConfigDict(use_enum_values=True)

    @abstractclassmethod
    def is_outdated(cls, memory_id: str) -> bool:
        """ 
            Check if the underlying data has changed since the last
            time this chunk was updated.

            For example, if the chunk is of type "github_repository", check 
            if the repository has been updated. If outdated, it should also
            propagate status to child nodes.
        """
        pass
