from abc import ABC, abstractmethod

class KV_Database(ABC):
    def __init__(self, *args, **kwargs):
        super().__init__()
        # Initialization can be arbitrary and flexible for subclass implementations.
    
    @abstractmethod
    def insert(self, category, key, value):
        """Insert a key-value pair."""
        pass

    @abstractmethod
    def set(self, category, key, value):
        """Set a value for a given key. Raise error if key exists."""
        pass

    @abstractmethod
    def update(self, category, key, updated_values):
        """Update the specified values for a given key. Raise error if key does not exist."""
        pass

    @abstractmethod
    def get(self, category, key):
        """Retrieve the value associated with a key."""
        pass

    @abstractmethod
    def delete(self, category, key):
        """Delete a key-value pair."""
        pass

    @abstractmethod
    def exists(self, category, key):
        """Check if a key exists."""
        pass

    @abstractmethod
    def append(self, category, key, value):
        """Append a value to a list associated with a key."""
        pass

    @abstractmethod
    def remove_from_list(self, category, key, value):
        """Remove a value from a list associated with a key."""
        pass