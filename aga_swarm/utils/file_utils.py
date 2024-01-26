'''
This is an internal utility module for loading files from package resources.
'''
import json
from importlib import resources
from typing import Any, BinaryIO, Optional

# Utility to get JSON data
def get_json_data(package: str, resource_name: str) -> Any:
    """
    Load a JSON file from the specified package resource.

    :param package: The package containing the resource.
    :param resource_name: The name of the JSON resource file.
    :return: Parsed JSON data.
    """
    with resources.open_text(package, resource_name) as file:
        return json.load(file)

# Utility to get binary data
def get_binary_data(package: str, resource_name: str) -> bytes:
    """
    Load binary data from a specified package resource.

    :param package: The package containing the resource.
    :param resource_name: The name of the binary resource file.
    :return: Binary data as bytes.
    """
    with resources.open_binary(package, resource_name) as file:
        return file.read()

# Utility to get a file-like object for binary data
def get_binary_file(package: str, resource_name: str) -> BinaryIO:
    """
    Get a file-like object for binary data from a specified package resource.

    :param package: The package containing the resource.
    :param resource_name: The name of the binary resource file.
    :return: File-like object for binary data.
    """
    return resources.open_binary(package, resource_name)

# Example usage
if __name__ == "__main__":
    # Replace 'my_package' with your actual package name
    json_data = get_json_data('my_package.data', 'config.json')
    binary_data = get_binary_data('my_package.data', 'image.png')

    print(json_data)
    # You can now use the binary_data or write it to a file, etc.
