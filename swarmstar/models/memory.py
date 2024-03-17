from typing import Union

from swarmstar.models.memory_metadata import MemoryMetadata
from swarmstar.utils.data import MongoDBWrapper
from swarmstar.models.internal_metadata import SwarmstarInternal

db = MongoDBWrapper()

class Memory:
    @staticmethod
    def get(memory_id: str) -> Union[bytes, str]:
        metadata = MemoryMetadata.get(memory_id)
        
        if metadata.is_folder:
            raise ValueError("Cannot get memory for a folder.")
        
        memory_type = metadata.type
        handler_mapping = {
            "folder": None,
            "internal_folder": None,
            "internal_string": Memory._internal_sqlite_retrieve,
            "project_root_folder": None,
            "project_file_bytes": Memory._simple_mongodb_retrieve,
            "string": Memory._simple_mongodb_retrieve
        }
        
        handler = handler_mapping[memory_type]
        return handler(memory_id)

    @staticmethod
    def save(memory_id: str, memory: Union[bytes, str]) -> None:
        metadata = MemoryMetadata.get(memory_id)
        memory_type = metadata.type
        handler_mapping = {
            "folder": None,
            "internal_folder": None,
            "internal_string": None,
            "project_root_folder": None,
            "project_file_bytes": Memory._simple_mongodb_insert,
            "string": Memory._simple_mongodb_insert
        }
        
        handler = handler_mapping[memory_type]
        handler(memory_id, memory)

    @staticmethod
    def delete(memory_id: str) -> None:
        metadata = MemoryMetadata.get(memory_id)
        memory_type = metadata.type
        handler_mapping = {
            "project_file_bytes": Memory._simple_mongodb_delete,
            "string": Memory._simple_mongodb_delete
        }
        db.delete("memory", memory_id)

    @staticmethod
    def _simple_mongodb_insert(memory_id: str, memory: Union[bytes, str]) -> None:
        db.insert("memory", memory_id, {"data": memory})

    @staticmethod
    def _simple_mongodb_retrieve(memory_id: str) -> Union[bytes, str]:
        return db.get("memory", memory_id)["data"]

    @staticmethod
    def _internal_sqlite_retrieve(memory_id: str) -> Union[bytes, str]:
        return SwarmstarInternal.get_internal_sqlite("memory", memory_id)
