from swarmstar.utils.data.internal_operations.internal_data import get_internal_metadata

def get_internal_action_metadata(action_id: str) -> dict:
    return get_internal_metadata("action_space", action_id)


def get_internal_memory_metadata(memory_id: str) -> dict:
    return get_internal_metadata("memory_space", memory_id)


def get_internal_util_metadata(util_id: str) -> dict:
    return get_internal_metadata("util_space", util_id)

