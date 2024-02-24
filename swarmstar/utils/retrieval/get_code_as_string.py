import importlib

from swarmstar.utils.retrieval.ast_chunking import find_class_start_end_lines
from swarmstar.utils.retrieval.get_lines import get_lines


def get_class_as_string(file_path: str, class_name: str) -> str:
    """
    Extracts the code for a class from a file.

    Parameters:
    - file_path: str - The path to the file from which to extract the code.
    - class_name: str - The name of the class to extract.

    Returns:
    - str - The extracted code as a string.
    """

    # Find the start and end lines of the class
    start_line, end_line = find_class_start_end_lines(file_path, class_name)

    # Extract the code for the class
    class_code = get_lines(file_path, (start_line, end_line))

    return class_code


def get_class_from_module(module_path: str, class_name: str):
    """
    Dynamically imports a class from a given module path and class name.

    :param module_path: A string representing the module path, relative to the package root, without the '.py' extension.
                        Example: 'my_package.my_module'
    :param class_name: The name of the class to import as a string.
    :return: The class type specified by class_name if found in the module; raises AttributeError otherwise.
    """
    try:
        # Dynamically import the module specified by module_path
        module = importlib.import_module(module_path)
        # Get the class specified by class_name from the imported module
        clazz = getattr(module, class_name)
        return clazz
    except ImportError as e:
        raise ImportError(f"Could not import module {module_path}: {e}") from None
    except AttributeError as e:
        raise AttributeError(
            f"Class {class_name} not found in module {module_path}: {e}"
        ) from None


# Example usage:
# Assuming there's a class MyClass in the module_path 'my_package.my_module'
# MyClass = get_class_from_module('my_package.my_module', 'MyClass')
