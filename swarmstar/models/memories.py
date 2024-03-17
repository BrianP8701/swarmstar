from swarmstar.models.memory_metadata import MemoryMetadata
from swarmstar.utils.data import MongoDBWrapper

db = MongoDBWrapper()

class Memory:
    
    @staticmethod
    def get_memory(memory_id: str) -> bytes:
        metadata = MemoryMetadata.get_memory_metadata(memory_id)
        
        if metadata.is_folder:
            raise ValueError("Cannot get memory for a folder.")
        
        memory_type = metadata.type
        handler_mapping = {
            "project_file_bytes": db.retrieve_bytes
        }
        
        handler = handler_mapping[memory_type]
        return handler("memories", memory_id)

    @staticmethod
    def save(memory_id: str, memory: bytes) -> None:
        metadata = MemoryMetadata.get_memory_metadata(memory_id)
        memory_type = metadata.type
        handler_mapping = {
            "project_file_bytes": db.save_bytes
        }
        
        handler = handler_mapping[memory_type]
        handler("memories", memory_id, memory)

    @staticmethod
    def delete(memory_id: str) -> None:
        metadata = MemoryMetadata.get_memory_metadata(memory_id)
        memory_type = metadata.type
        handler_mapping = {
            "project_file_bytes": db.delete
        }
        
        handler = handler_mapping[memory_type]
        handler("memories", memory_id)