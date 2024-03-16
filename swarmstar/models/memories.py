from swarmstar.models.memory_metadata import MemoryMetadata
from swarmstar.utils.data import MongoDBWrapper

db = MongoDBWrapper()

class Memory:
    
    @staticmethod
    def get_memory(memory_id: str) -> bytes:
        metadata = MemoryMetadata.get_memory_metadata(memory_id)
        
        if metadata.is_folder:
            raise ValueError("Cannot get memory for a folder.")
        
        memory_type = metadata.memory_type
        handler_mapping = {
            "project_file_bytes": db.retrieve_bytes
        }
        
        handler = handler_mapping[memory_type]
        return handler(memory_id)
