from abc import ABC, abstractmethod
import json
from typing import Any

class FileStorage(ABC):
    def __init__(self, *args, **kwargs):
        super().__init__()
        # Initialization can be arbitrary and flexible for subclass implementations.

    @abstractmethod
    def validate_path(self, path: str) -> bool:
        """Validate a path according to the storage."""
        pass

    @abstractmethod
    def save_file(self, path: str, content: bytes) -> None:
        """Save content to a file."""
        pass

    @abstractmethod
    def read_file_as_string(self, path: str) -> str:
        """Read file content as a string."""
        pass

    @abstractmethod
    def delete_file(self, path: str) -> None:
        """Delete a file."""
        pass

    @abstractmethod
    def file_exists(self, path: str) -> bool:
        """Check if a file exists."""
        pass

    @abstractmethod
    def append_to_file(self, path: str, content: bytes) -> None:
        """Append content to a file."""
        pass

    @abstractmethod
    def make_folder(self, path: str) -> None:
        """Create a new folder at the specified path."""
        pass

    @abstractmethod
    def delete_folder(self, path: str) -> None:
        """Delete the folder and all its contents at the specified path."""
        pass
