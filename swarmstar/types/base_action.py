"""
This module contains the base class for all actions.
This base class: 

    - Provides some common methods that actions use.
    - Provides a metaclass to apply an error handling decorator to all methods of the action.
    
When a new action is created, it should subclass BaseAction and implement the main method.

All action functions will automatically be wrapped with the error handling decorator, which 
will catch any exceptions and return a FailureOperation with a report of the error.
"""
import traceback
from abc import ABCMeta, abstractmethod
from functools import wraps
from typing import Any, Dict, List, Callable, get_type_hints, get_origin, get_args
from inspect import signature

from swarmstar.utils.swarmstar_space import update_swarm_node
from swarmstar.types.swarm_config import SwarmConfig
from swarmstar.types.swarm_node import SwarmNode
from swarmstar.types.swarm_operations import SwarmOperation


def error_handling_decorator(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            self = args[
                0
            ]  # Assuming the first argument is always 'self' for instance methods
            tb_str = traceback.format_exc()
            params_str = f"node_id: {self.node.id}\nParams: {kwargs}"

            error_message = (
                f"Error in {func.__name__}:\n{str(e)}\n\n{tb_str}\n\n{params_str}"
            )
            raise Exception(error_message)

            # TODO Failure Operation for error handling
            # return FailureOperation(
            #     node_id=self.node.id,
            #     report=report,
            # )

    return wrapper


class ErrorHandlingMeta(ABCMeta):
    def __new__(mcs, name, bases, dct):
        new_cls = super().__new__(mcs, name, bases, dct)
        for attr_name, attr_value in dct.items():
            if callable(attr_value) and not attr_name.startswith("__"):
                error_wrapped = error_handling_decorator(attr_value)
                setattr(new_cls, attr_name, error_wrapped)
        return new_cls

class BaseAction(metaclass=ErrorHandlingMeta):
    """
    All actions should subclass this class.
    """

    def __init__(self, swarm_config: SwarmConfig, node: SwarmNode):
        self.swarm_config = swarm_config
        self.node = node

    @abstractmethod
    def main(self) -> [SwarmOperation, List[SwarmOperation]]:
        pass

    def report(self, report: str):
        self.node.report = report
        update_swarm_node(self.swarm_config, self.node)
    
    def update_termination_policy(self, termination_policy: str):
        self.node.termination_policy = termination_policy
        update_swarm_node(self.swarm_config, self.node)
        
    @staticmethod
    def termination_handler(func: Callable):
        def wrapper(self, terminator_node_id: str, context: Dict[str, Any]):
            sig = signature(func)
            params = sig.parameters
            if len(params) != 3 or list(params.keys()) != ['self', 'terminator_node_id', 'context']:
                raise TypeError("Function must accept exactly two parameters: 'terminator_node_id' and 'context', along with 'self'")
            
            # Check return type using type hints
            type_hints = get_type_hints(func)
            if 'return' in type_hints:
                return_type = type_hints['return']
                if get_origin(return_type) is list:  # Check if the return type is a generic list
                    if not issubclass(get_args(return_type)[0], SwarmOperation):
                        raise TypeError("Return type must be SwarmOperation or List[SwarmOperation]")
                elif not issubclass(return_type, SwarmOperation):  # Direct class check if not a generic list
                    raise TypeError("Return type must be SwarmOperation or List[SwarmOperation]")
            
            # Call the actual function
            return func(self, terminator_node_id, context)
        return wrapper

    def log(self, log_dict: Dict[str, Any], index_key: List[int] = None) -> List[int]:
        """
        This function appends a log to the developer_logs list in a node or a nested list 
        within developer_logs.

        The log_dict should have the following format:
        {
            "role": (swarmstar, system, ai or user),
            "content": "..."
        }
        
        If you are not doing parallel logs, you can ignore the index_key parameter.
        Parallel logs are logs that were performed in parallel. For example, if within 
        one node we have multiple conversations in parallel, we don't want these to 
        overlap in the logs.
        
        Example:

        [log0, log1, log2, [log3.0, log3.1, log3.2], log4]
            log3.0, log3.1, log3.2 are grouped.

        or even,

        [log0, log1, [[log2.0.0, log2.0.1, log2.0.2], [log2.1.0, log2.1.1]], log3]
            log2.0.0, log2.0.1, log2.0.2 are grouped.
            log2.1.0, log2.1.1 are grouped.
            log2.0 and log2.1 are performed in parallel.

        If index_key is None, the log will be appended to the developer_logs list.
        If an index_key is provided, the log will be appended to the nested list at the index_key.

        The function can create a new empty list and add the log if the list doesn't exist,
        but it can only create one list at a time. If an attempt is made to create more than one list
        at a time, an error will be raised.

        :param log_dict: A dictionary representing the log to be added.
        :param index_key: A list of integers representing the index path to the nested list where the log should be added.
        :raises ValueError: If an attempt is made to create more than one list at a time.

        :return: The index_key of the log that was added.
        """
        if index_key is None:
            self.node.developer_logs.append(log_dict)
            return_index_key = [len(self.node.developer_logs) - 1]
        else:
            nested_list = self.node.developer_logs
            for i, index in enumerate(index_key):
                if index > len(nested_list):
                    raise IndexError(f"Index {index} is out of range for the current list. {nested_list}")
                if i == len(index_key) - 1:
                    if len(nested_list) == index:
                        nested_list.append([log_dict])
                        return_index_key = index_key + [0]
                    elif isinstance(nested_list[index], list):
                        nested_list[index].append(log_dict)
                        return_index_key = index_key + [len(nested_list[index]) - 1]
                    else:
                        nested_list[index] = [nested_list[index], log_dict]
                        return_index_key = index_key + [1]
                else:
                    if isinstance(nested_list[index], list):
                        nested_list = nested_list[index]
                    else:
                        raise ValueError("Invalid index_key. Cannot traverse non-list elements.")
        update_swarm_node(self.swarm_config, self.node)
        return return_index_key
