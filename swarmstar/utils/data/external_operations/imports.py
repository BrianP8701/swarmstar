import importlib.util
import sys
from pathlib import Path

def import_module_from_path(module_name: str, path_to_file: str):
    """
    Dynamically imports a module relative to the runtime's current working directory.
    
    Args:
        module_name (str): The name to assign to the module.
        path_to_file (str): The path to the module file, can be absolute or relative to the current working directory.
    
    Returns:
        A module object if the import is successful. None otherwise.
    """
    module_path = Path(path_to_file).resolve()  # Ensures the path is absolute
    spec = importlib.util.spec_from_file_location(module_name, str(module_path))
    if spec is None:
        return None
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module