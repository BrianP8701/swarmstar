from abc import ABC, abstractmethod
from typing import Any, Dict, List

class Database(ABC):
    def __init__(self, *args, **kwargs):
        # Initialization can be arbitrary and flexible for subclass implementations.
        super().__init__()

    """                      CRUD operations                         """
    @abstractmethod
    def create(self, category: str, key: str, value: Dict[str, Any]) -> None:
        """Insert a key-value pair. Raise error if key already exists."""
        pass

    @abstractmethod
    def read(self, category: str, key: str) -> Dict[str, Any]:
        """Read the value associated with a key."""
        pass

    @abstractmethod
    def update(self, category: str, key: str, updated_fields: Dict[str, Any]) -> None:
        """Update the specified fields for a given key. Raise error if key does not exist."""
        pass

    @abstractmethod
    def delete(self, category: str, key: str) -> None:
        """Delete a key-value pair."""
        pass



    """              Managing transaction sessions for atomicity              """
    @abstractmethod
    def begin_transaction(self) -> Any:
        """Start and return a transaction session."""
        pass

    @abstractmethod
    def commit_transaction(self) -> None:
        """Commit a transaction session."""
        pass

    @abstractmethod
    def rollback_transaction(self) -> None:
        """Rollback a transaction session."""
        pass



    """                     Locks                     """
    @abstractmethod
    def lock(self, category: str, key: str) -> None:
        """ Lock a key. Raise error if key is already locked. """
        pass

    @abstractmethod
    def unlock(self, category: str, key: str) -> None:
        """Unlock a key."""
        pass



    """                     Other common operations.                     """
    @abstractmethod
    def replace(self, category: str, key: str, value: Any) -> None:
        """ Replace a value for a given key. Raise error if key does not exist. """
        pass

    @abstractmethod
    def copy(self, category: str, key: str, new_key: str) -> None:
        """ Copy a key-value pair to a new key. Raise error if key does not exist. """
        pass

    @abstractmethod
    def get_field(self, category: str, key: str, field: str) -> Any:
        """ Grab the value associated with a specified field inside the document. """
        pass

    @abstractmethod
    def exists(self, category: str, key: str) -> bool:
        """ Check if a document exists. """
        pass

    @abstractmethod
    def increment(self, category: str, key: str, field: str, amount: int = 1) -> int:
        """Increment a value stored under a specified field, returning the original value."""
        pass

    @abstractmethod
    def pop_field(self, category: str, key: str, field: str) -> Any:
        """ Remove and return the specified field in the document. """
        pass



    """                     List operations                     """
    @abstractmethod
    def append(self, category: str, key: str, field: str, value: Any) -> None:
        """ Append a value to a list stored under a specified field. """
        pass

    @abstractmethod
    def remove_from_array_at_index(self, category: str, key: str, field: str, index: int) -> None:
        """ Remove the index in a list at the specified field. """
        pass

    @abstractmethod
    def remove_value_from_array(self, category: str, key: str, field: str, value: Any) -> None:
        """ Remove specified value from a list stored under a specified field. """
        pass

    @abstractmethod
    def pop_array(self, category: str, key: str, field: str, index: int = -1) -> Any:
        """ Remove and return the value at the index (default: -1) in the list stored under a specified field. """
        pass

    @abstractmethod
    def array_length(self, category: str, key: str, field: str) -> int:
        """ Return the length of the list stored under a specified field. """
        pass


    """                     Batch operations                     """
    @abstractmethod
    def batch_create(self, category: str, keys: Dict[str, Dict[str, Any]]) -> None:
        """ Insert multiple key-value pairs. Raise error if any key already exists. """
        pass

    @abstractmethod
    def batch_read(self, category: str, keys: List[str]) -> Dict[str, Dict[str, Any]]:
        """ Read multiple values associated with the keys. Returns a dictionary of key-value pairs. """
        pass

    @abstractmethod
    def batch_update(self, category: str, updated_fields: Dict[str, Dict[str, Any]]) -> None:
        """ Update multiple keys with specified fields. Raise error if any key does not exist. """
        pass

    @abstractmethod
    def batch_delete(self, category: str, keys: List[str]) -> None:
        """ Delete multiple key-value pairs. """
        pass

    @abstractmethod
    def batch_copy(self, category: str, keys: List[str], new_keys: List[str]) -> None:
        """ Copy multiple key-value pairs to new keys. Raise error if any key does not exist. """
        pass
