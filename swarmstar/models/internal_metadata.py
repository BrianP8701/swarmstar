from swarmstar.utils.data.internal_operations.internal_sqlite import get_internal_sqlite

class SwarmstarInternal:
    """
        This class provides methods to read metadata from the 
        internal sqlite database.
    """
    @staticmethod
    def get_action_metadata(action_id: str) -> dict:
        return get_internal_sqlite("action_space", action_id)

    @staticmethod
    def get_memory_metadata(memory_id: str) -> dict:
        return get_internal_sqlite("memory_space", memory_id)

    @staticmethod
    def get_util_metadata(util_id: str) -> dict:
        return get_internal_sqlite("util_space", util_id)
