"""
This module provides the BaseAction class, which all actions must inherit from.

The BaseAction class provides a number of methods and decorators to make it easier to write actions.
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

from swarmstar.models import SwarmOperation, SwarmNode, SpawnOperation, NodeEmbryo, BaseNode


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
        if self.node.report is not None:
            raise ValueError(f"Node {self.node.id} already has a report: {self.node.report}. Cannot update with {report}.")
        self.node.report = report
        SwarmNode.replace(self.node.id, self.node)
    
    def update_termination_policy(self, termination_policy: str):
        self.node.termination_policy = termination_policy
        SwarmNode.replace(self.node.id, self.node)
    
    def add_value_to_execution_memory(self, attribute: str, value: Any):
        self.node.execution_memory[attribute] = value
        SwarmNode.replace(self.node.id, self.node)
    
    def remove_value_from_execution_memory(self, attribute: str):
        del self.node.execution_memory[attribute]
        SwarmNode.replace(self.node.id, self.node)

    def update_execution_memory(self, execution_memory: Dict[str, Any]):
        self.node.execution_memory = execution_memory
        SwarmNode.replace(self.node.id, self.node)

    def clear_execution_memory(self):
        self.node.execution_memory = {}
        SwarmNode.replace(self.node.id, self.node)

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
        This wrapper will be called multiple times, and at each step will be in one of the following stages.
        This wrapper will know which stage it is in by checking the received parameters.

        1. Giving the LLM the option to ask questions:
            Expected parameters: message: str, Optional[context: Dict[str, Any]]
        - Adds a `questions` attribute (List[str]) to the pydantic model.
        - Makes every attribute optional.
        - Appends a prompt emphasizing the importance of asking questions when necessary.
        - Sets the blocking operation's `next_function_to_call` to the wrapped function.
        - Stores the intended next function and message in the context.
        - Returns the blocking operation to be executed.

        2. Accessing the oracle:
            Expected parameters: (completion: Any, context: Dict[str, Any])
        - Checks if the `questions` field in the completion is None.
        - If None, calls the intended next function with the completion.
        - If not None, spawns an oracle node to answer the questions.
        - Set this node's termination handler to the wrapped function.

        3. Handling the oracle's completion:
            Expected parameters: (terminator_node_id: str, context: Dict[str, Any])
        - Appends the questions and answers from the oracle node to the original message.
        - Retries the blocking operation with the updated context.

        This process repeats until the LLM makes a decision without asking further questions.
        """
        @wraps(func)
        def wrapper(self, **kwargs):
            message = kwargs.pop("message", None)
            context = kwargs.pop("context", None)
            completion = kwargs.get("completion", None)
            if type(completion) is not dict: completion = completion.model_dump()
            terminator_node_id = kwargs.get("terminator_node_id", None)
            
            if message: # Stage 1
                if context: blocking_operation = func(self, message, context)
                else: blocking_operation = func(self, message)
                blocking_operation.context["__next_function_to_call__"] = blocking_operation.next_function_to_call
                blocking_operation.next_function_to_call = func.__name__
                blocking_operation.context["__message__"] = message
                blocking_operation.context["__oracle_access__"] = True
            elif completion and context: # Stage 2
                if completion.questions is None:
                    __next_function_to_call__ = context.pop("__next_function_to_call__", None)
                    context.pop("__message__", None)
                    if context: return getattr(self, __next_function_to_call__)(completion, context)
                    else: return getattr(self, __next_function_to_call__)(completion)
                else:
                    self.update_termination_policy("custom_termination_handler")
                    self.update_execution_memory({"__termination_handler__": func.__name__})
                    context["__questions__"] = completion.questions
                    return SpawnOperation(
                        parent_node_id=self.node.id,
                        node_embryo=NodeEmbryo(
                            action_id="specific/oracle",
                            message={
                                "questions": completion.questions, 
                                "context": completion.context
                            },
                            context=context
                        )
                    )
            elif terminator_node_id: # Stage 3
                terminator_node = BaseNode.get(terminator_node_id)
                question_answers = terminator_node.context
                questions = terminator_node.context["__questions__"]
                message = terminator_node.context["__message__"]
                message += f"\n\n{questions}\n\n{question_answers}"
                return func(self, message, context)
            else:
                raise ValueError(f"oracle_access wrapper called with invalid parameters: {kwargs}")
        return wrapper


# Look at this again later # TODO for some reason its repeating stuff and outputs a ton of shit
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
#             #         action_id="swarmstar/actions/swarmstar/handle_failure",
#             #         message=error_message,
#             #         context={'error_details': error_details}
#             #     )
#             # )
    
#     return wrapper