'''
    Functions for getting default stuff from
    the aga_swarm package.
'''

from importlib import import_module
import json
from importlib import resources
from typing import Any, BinaryIO

def get_default_action_space_metadata() -> dict:
    return get_json_data('aga_swarm.actions', 'action_space_metadata.json')

def get_default_memory_space_metadata() -> dict: 
    return get_json_data('aga_swarm.memory', 'memory_space_metadata.json')

def import_internal_python_action(module_name):
    '''
    This function imports the main function from a python script.
    Meant to be used for importing internal python actions.
    '''
    module_name = module_name.replace('/', '.')
    module_name = module_name.replace('.py', '')
    module = import_module(module_name)
    main = getattr(module, 'main', None)  
    if main is None:
        raise AttributeError(f"No main function found in the script {module_name}")
    return main

def get_json_data(package: str, resource_name: str) -> Any:
    """
    Load a JSON file from the specified package resource.

    :param package: The package containing the resource.
    :param resource_name: The name of the JSON resource file.
    :return: Parsed JSON data.
    """
    with resources.open_text(package, resource_name) as file:
        return json.load(file)

def get_binary_data(package: str, resource_name: str) -> bytes:
    """
    Load binary data from a specified package resource.

    :param package: The package containing the resource.
    :param resource_name: The name of the binary resource file.
    :return: Binary data as bytes.
    """
    with resources.open_binary(package, resource_name) as file:
        return file.read()

def get_binary_file(package: str, resource_name: str) -> BinaryIO:
    """
    Get a file-like object for binary data from a specified package resource.

    :param package: The package containing the resource.
    :param resource_name: The name of the binary resource file.
    :return: File-like object for binary data.
    """
    return resources.open_binary(package, resource_name)
