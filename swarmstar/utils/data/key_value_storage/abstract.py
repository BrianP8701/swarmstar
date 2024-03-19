from abc import ABC, abstractmethod
from typing import Any, Dict

class KV_Database(ABC):
    def __init__(self, *args, **kwargs):
        super().__init__()
        # Initialization can be arbitrary and flexible for subclass implementations.
    
    @abstractmethod
    def insert(self, category: str, key: str, value: Any):
        """Insert a key-value pair. Raise error if key already exists."""
        pass

    @abstractmethod
    def replace(self, category: str, key: str, value: Any):
        """Replace a value for a given key. Raise error if key does not exist."""
        pass

    @abstractmethod
    def update(self, category: str, key: str, updated_values: Dict[str, Any]):
        """Update the specified values for a given key. Raise error if key does not exist."""
        pass

    @abstractmethod
    def get(self, category: str, key: str) -> Dict[str, Any]:
        """Retrieve the value associated with a key."""
        pass

    @abstractmethod
    def get_by_key(self, category: str, key: str, inner_key: str) -> Any:
        """Retrieve the value associated with a specified key inside the document."""
        pass

    @abstractmethod
    def delete(self, category: str, key: str) -> None:
        """Delete a key-value pair."""
        pass

    @abstractmethod
    def exists(self, category: str, key: str) -> bool:
        """Check if a key exists."""
        pass

    @abstractmethod
    def append_to_list(self, category: str, key: str, inner_key: str, value: Any):
        """Append a value to a list stored under a specified key. If the key does not exist, create a new list with the value."""
        pass

    @abstractmethod
    def remove_from_list(self, category: str, key: str, inner_key: str, value: Any):
        """Remove a value from a list stored under a specified key."""
        pass
