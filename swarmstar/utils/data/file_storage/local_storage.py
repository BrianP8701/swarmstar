import os
import shutil

from swarmstar.utils.context import root_path_var

class LocalStorage:
    _instance = None

    root_path = root_path_var.get()  # Retrieve the root path from the context variable


    def __new__(cls, root_path: str):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.root_path = root_path
        return cls._instance

    def save_file(self, path: str, content: bytes) -> None:
        """Save content to a file."""
        try:
            full_path = os.path.join(self.root_path, path)
            with open(full_path, 'wb') as file:
                file.write(content)
        except OSError as e:
            raise Exception(f"Error saving file: {str(e)}")

    def read_file_as_string(self, path: str) -> str:
        """Read file content as a string."""
        try:
            full_path = os.path.join(self.root_path, path)
            with open(full_path, 'r') as file:
                return file.read()
        except FileNotFoundError:
            raise Exception(f"File not found: {path}")
        except OSError as e:
            raise Exception(f"Error reading file: {str(e)}")

    def delete_file(self, path: str) -> None:
        """Delete a file."""
        try:
            full_path = os.path.join(self.root_path, path)
            if os.path.exists(full_path):
                os.remove(full_path)
            else:
                raise FileNotFoundError(f"File not found: {path}")
        except OSError as e:
            raise Exception(f"Error deleting file: {str(e)}")

    def file_exists(self, path: str) -> bool:
        """Check if a file exists."""
        try:
            full_path = os.path.join(self.root_path, path)
            return os.path.exists(full_path)
        except OSError as e:
            raise Exception(f"Error checking file existence: {str(e)}")

    def append_to_file(self, path: str, content: bytes) -> None:
        """Append content to a file."""
        try:
            full_path = os.path.join(self.root_path, path)
            with open(full_path, 'ab') as file:
                file.write(content)
        except OSError as e:
            raise Exception(f"Error appending to file: {str(e)}")

    def make_folder(self, path: str) -> None:
        """Create a new folder at the specified path."""
        try:
            full_path = os.path.join(self.root_path, path)
            os.makedirs(full_path, exist_ok=True)
        except OSError as e:
            raise Exception(f"Error creating folder: {str(e)}")

    def delete_folder(self, path: str) -> None:
        """Delete the folder and all its contents at the specified path."""
        try:
            full_path = os.path.join(self.root_path, path)
            if os.path.exists(full_path):
                shutil.rmtree(full_path)
            else:
                raise FileNotFoundError(f"Folder not found: {path}")
        except OSError as e:
            raise Exception(f"Error deleting folder: {str(e)}")
