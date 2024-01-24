import sys
import json
from typing import Dict, Type

def validate_action_args(schema: Dict[str, Type]):
    """
    Validates that arguments passed to action are valid

    :param schema: A dictionary where keys are the expected keys in the args_dict
                   and values are the expected types of these keys.
    :return: Parsed arguments dictionary if validation is successful.
    :raises: ValueError if validation fails.
    """
    if len(sys.argv) != 2:
        raise ValueError("Expected exactly one argument.")

    try:
        args_dict = json.loads(sys.argv[1])
    except json.JSONDecodeError:
        raise ValueError("Argument is not valid JSON.")

    if not isinstance(args_dict, dict):
        raise ValueError("Argument is not a JSON dictionary.")

    for key, expected_type in schema.items():
        if key not in args_dict:
            raise ValueError(f"Missing expected key: '{key}'")

        if not isinstance(args_dict[key], expected_type):
            raise ValueError(f"Key '{key}' is not of type {expected_type.__name__}")

    return args_dict