from swarmstar.utils.data import get_internal_memory_metadata, get_kv
from swarmstar.swarm.types import SwarmConfig, MemoryMetadata

def get_memory_metadata(swarm: SwarmConfig, memory_id: str) -> MemoryMetadata:
    try:
        memory_metadata = get_internal_memory_metadata(memory_id)
        if action_metadata is None:
            raise ValueError(
                f"This memory id: `{memory_id}` does not exist in internal memory space."
            )
    except Exception as e1:
        try:
            memory_metadata = get_kv(swarm, "memory_space", memory_id)
            if memory_metadata is None:
                raise ValueError(
                    f"This memory id: `{memory_id}` does not exist in external memory space."
                ) from e1
        except Exception as e2:
            raise ValueError(
                f"This memory id: `{memory_id}` does not exist in both internal and external memory spaces."
            ) from e2

    type_mapping = {
        "internal_memory": InternalMemory,
        "internal_folder": InternalFolder,
    }
    memory_type = memory_metadata["type"]
    if memory_type in type_mapping:
        return type_mapping[memory_type](**memory_metadata)
    return MemoryNode(**memory_metadata)
