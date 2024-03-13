from swarmstar.utils.data.internal_operations.internal_sqlite import get_internal_sqlite

class SwarmstarInternal:
    @staticmethod
    def get_internal_action_metadata(action_id: str) -> dict:
        return get_internal_sqlite("action_space", action_id)

    @staticmethod
    def get_internal_memory_metadata(memory_id: str) -> dict:
        return get_internal_sqlite("memory_space", memory_id)

    @staticmethod
    def get_internal_util_metadata(util_id: str) -> dict:
        return get_internal_sqlite("util_space", util_id)
