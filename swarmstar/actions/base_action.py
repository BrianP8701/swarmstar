"""
This module contains the base class for all actions.
This base class: 

    - Provides some common methods that actions use.
    - Provides a metaclass to apply an error handling decorator to all methods of the action.
    
When a new action is created, it should subclass BaseAction and implement the main method.

All action functions will automatically be wrapped with the error handling decorator, which 
will catch any exceptions and return a FailureOperation with a report of the error.
"""
from importlib import import_module
import traceback
from abc import ABCMeta, abstractmethod
from functools import wraps
from typing import Any, Dict, List, Callable, get_type_hints, get_origin, get_args
from inspect import signature
import json
import sys
import inspect

from swarmstar.models import SwarmOperation, SwarmNode, SpawnOperation, NodeEmbryo


# def error_handling_decorator(func):
#     @wraps(func)
#     def wrapper(self, *args, **kwargs):
#         try:
#             return func(self, *args, **kwargs)
#         except Exception as e:
#             exc_type, exc_value, exc_traceback = sys.exc_info()
#             traceback_str = ''.join(traceback.format_exception(exc_type, exc_value, exc_traceback))
            
#             # Capture local variables
#             frame = inspect.trace()[-1][0]
#             local_vars = frame.f_locals
            
#             error_details = {
#                 'exc_type': exc_type.__name__,
#                 'exc_value': str(exc_value),
#                 'exc_traceback': traceback_str,
#                 'local_variables': {key: repr(value) for key, value in local_vars.items()},
#                 'error_line': frame.f_lineno,
#                 'error_module': frame.f_code.co_filename
#             }
            
#             error_message = (
#                 f"Error in {func.__name__}:\n{str(e)}\n\n"
#                 f"Traceback:\n{traceback_str}\n\n"
#                 f"Local Variables:\n{json.dumps(error_details['local_variables'], indent=2)}"
#             )
            
#             raise ValueError(error_message)
#             # return SpawnOperation(
#             #     parent_node_id=self.node.id,
#             #     node_embryo=NodeEmbryo(
#             #         # TODO When u make failure action change this
#             #         action_id="swarmstar/actions/swarmstar/handle_failure",
#             #         message=error_message,
#             #         context={'error_details': error_details}
#             #     )
#             # )
    
#     return wrapper

def error_handling_decorator(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        try:
            return func(self, *args, **kwargs)
        except Exception as e:
            error_message = (
                f"Error in {func.__name__}:\n"
                f"Type: {type(e).__name__}\n"
                f"Message: {str(e)}\n"
                f"File: {e.__traceback__.tb_frame.f_code.co_filename}\n"
                f"Line: {e.__traceback__.tb_lineno}\n"
            )
            raise ValueError(error_message)
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

    def __init__(self, node: SwarmNode):
        self.node = node

    @abstractmethod
    def main(self) -> [SwarmOperation, List[SwarmOperation]]:
        pass        
    
    def get_node(self) -> SwarmNode:
        return SwarmNode.get(self.node.id)
    
    def report(self, report: str):
        node = self.get_node()
        if node.report is not None:
            raise ValueError(f"Node {node.id} already has a report: {node.report}. Cannot update with {report}.")
        node.report = report
        SwarmNode.replace(node)
    
    def update_termination_policy(self, termination_policy: str):
        node = self.get_node()
        node.termination_policy = termination_policy
        SwarmNode.replace(node)
    
    def add_value_to_execution_memory(self, attribute: str, value: Any):
        node = self.get_node()
        node.execution_memory[attribute] = value
        SwarmNode.replace(node)
    
    def remove_value_from_execution_memory(self, attribute: str):
        node = self.get_node()
        del node.execution_memory[attribute]
        SwarmNode.replace(node)

    def update_execution_memory(self, execution_memory: Dict[str, Any]):
        node = self.get_node()
        node.execution_memory = execution_memory
        SwarmNode.replace(node)

    def clear_execution_memory(self):
        node = self.get_node()
        node.execution_memory = {}
        SwarmNode.replace(node)
    
    @staticmethod
    def termination_handler(func: Callable):
        """
            This decorator is used to mark a function as a termination handler.
            
            When termination policy is set to "custom_action_termination", it is expected 
            that the action will set __termination_handler__ in the node's execution memory 
            to the name of the function that will handle the termination. This function
            should be wrapped with this decorator, to ensure it has the correct signature.
        """
        def wrapper(self, **kwargs):
            terminator_node_id = kwargs["terminator_node_id"]
            context = kwargs["context"]
            
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

    @staticmethod
    def receive_completion_handler(func: Callable):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            if len(args) > 1:
                # If there are positional arguments, convert them to keyword arguments
                arg_names = list(signature(func).parameters.keys())[1:]  # Exclude 'self'
                for arg_name, arg_value in zip(arg_names, args[1:]):
                    if arg_name not in kwargs:
                        kwargs[arg_name] = arg_value
                args = args[:1]  # Keep only 'self'

            completion = kwargs.get("completion")
            sig = signature(func)
            params = sig.parameters
            instructor_model_name = kwargs.pop("instructor_model_name", None)

            if type(completion) is dict and instructor_model_name:
                models_module = import_module("swarmstar.actions.pydantic_models")
                instructor_model = getattr(models_module, instructor_model_name)
                completion = instructor_model.model_validate(completion)
                kwargs["completion"] = completion

            # Extract the required arguments from kwargs based on the function signature
            func_args = {}
            for param in params.values():
                if param.name != "self":
                    if param.name in kwargs:
                        func_args[param.name] = kwargs.pop(param.name)
                    elif param.default != param.empty:
                        func_args[param.name] = param.default

            return func(self, *args, **func_args)
        return wrapper
