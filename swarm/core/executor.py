import importlib.util
import sys
import os

def execute(node):
    """
    Executes the 'main' function from a script located in the given folder path
    and returns its result.

    :param folder_path: Path to the folder containing the script.
    :param args_dict: Dictionary of arguments to pass to the script's main function.
    :return: The result of the script's main function.
    """
    path_prefix = 'swarm/actions/'
    folder_path = node.type
    args_dict = node.data

    action_path = os.path.join(path_prefix, folder_path)

    # Append script.py to the folder path
    script_path = os.path.join(action_path, 'script.py')

    # Check if the script exists
    if not os.path.exists(script_path):
        raise FileNotFoundError(f"No script found at path: {script_path}")

    # Prepare the module spec
    spec = importlib.util.spec_from_file_location("module.name", script_path)

    # Load the module
    module = importlib.util.module_from_spec(spec)

    # Add the folder path to sys.path for relative imports in the script
    sys.path.append(action_path)

    # Execute the module
    spec.loader.exec_module(module)

    # Check if the module has a 'main' function
    if not hasattr(module, 'main'):
        raise AttributeError("The script does not have a 'main' function.")

    # Call the 'main' function with the provided arguments and return its result
    return module.main(**args_dict)