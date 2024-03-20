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
    def wrapper(self, **kwargs):
        try:
            return func(self, **kwargs)
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
    All actions should inherit this class.
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
    def custom_termination_handler(func: Callable):
        """
            This decorator is used to mark a function as a custom termination handler. It simply enforces the function parameters.

            Functions marked with this decorator should accept two parameters:
                - terminator_node_id: The id of the terminator node that this node spawned
                - context: Context persisted from spawning the terminator node

            This allows us to easily spawn new nodes, and then respond to te termination of those nodes.
        """
        def wrapper(self, **kwargs):
            terminator_node_id = kwargs.pop("terminator_node_id", None)
            context = kwargs.pop("context", None)
            
            if not terminator_node_id:
                raise ValueError(f"terminator_node_id is a required parameter for custom_termination_handler. Error in {self.node.id} at function {func.__name__}")
            if not context:
                raise ValueError(f"context is a required parameter for custom_termination_handler. Error in {self.node.id} at function {func.__name__}")

            return func(self, terminator_node_id, context)
        return wrapper

    @staticmethod
    def receive_instructor_completion_handler(func: Callable):
        @wraps(func)
        def wrapper(self, **kwargs):
            """
            This wrapper is used on any action function that is meant 
            to handle the completion of an instructor_completion.
            
            The function should accept two parameters as keyword arguments:
                - completion: The completion of the instructor_completion of type defined by the instructor_model_name
                - context: Context persisted through the blocking operation. Optional.
            
            (Skip this if not interested)
            In an action we'll output a blocking operation. When this operation is executed, it'll
            return an action operation with the response. Instructor completions return a response
            following the specified Pydantic model. However, if we pause the swarm, the action operation
            will get serialized, converting the completion into a dictionary. This wrapper merely ensures
            that the completion is converted back into the Pydantic model before being passed to the function
            in case of this scenario.
            """
            completion = kwargs.get("completion", None)
            context = kwargs.get("context", None)
            instructor_model_name = kwargs.pop("instructor_model_name", None)

            if not instructor_model_name or not completion:
                raise ValueError(f"instructor_model_name and completion are required parameters for receive_instructor_completion_handler. Error in {self.node.id} at function {func.__name__}")

            if type(completion) is dict and instructor_model_name:
                models_module = import_module("swarmstar.utils.ai.instructor_models")
                instructor_model = getattr(models_module, instructor_model_name)
                completion = instructor_model.model_validate(completion)

            if context:
                return func(self, completion, context)
            else:
                return func(self, completion)
        return wrapper

    @staticmethod
    def oracle_access(func: Callable):
        """
        Decorator to mark a function as one that requires access to an oracle.

        The oracle is responsible for answering questions and has access to the swarm's memory,
        the internet, and can communicate with the user as a last resort. 
    
        This abstracts the RAG problem away from actions. To ensure any action is performed
        with full context, we tell the LLM to ask questions. The answering of these questions
        is the oracle's responsibility.

        Functionality:
        1. Giving the LLM the option to ask questions:
        - Adds a `questions` attribute (List[str]) to the pydantic model.
        - Makes every attribute optional.
        - Appends a prompt emphasizing the importance of asking questions when necessary.
        - Sets the blocking operation's `next_function_to_call` to the wrapped function.
        - Stores the intended next function and message in the context.

        2. Accessing the oracle:
        - Checks if the `questions` field in the completion is None.
        - If None, calls the intended next function with the completion.
        - If not None, spawns an oracle node to answer the questions.
        - Sets the oracle node's termination handler to the wrapped function.

        3. Handling the oracle's completion:
        - Appends the questions and answers from the oracle node to the original message.
        - Retries the blocking operation with the updated context.

        This process repeats until the LLM makes a decision without asking further questions.
        """
        @wraps(func)
        def wrapper(self, **kwargs):
            message = kwargs.pop("message", None)
            context = kwargs.pop("context", None)
            if not message:
                raise ValueError(f"message is a required parameter for oracle_access. Error in {self.node.id} at function {func.__name__}")
            if context:
                result = func(self, message, context)
            else:
                result = func(self, message)

            # Post-function logic
            print("Post-function logic here")
            return result
        return wrapper
