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

from swarmstar.models import SwarmOperation, SwarmNode, SpawnOperation, BaseNode, ActionMetadata, BlockingOperation

def error_handling_decorator(func):
    @wraps(func)
    def wrapper(self, **kwargs):
        try:
            return func(self, **kwargs)
        except Exception as e:
            error_type = type(e).__name__
            error_message = str(e)
            traceback_info = traceback.format_exc()
            
            error_details = (
                f"Error in {func.__name__}:\n"
                f"Type: {error_type}\n"
                f"Message: {error_message}\n"
                f"Traceback:\n{traceback_info}"
            )
            raise ValueError(error_details)
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
        return SwarmNode.read(self.node.id)
    
    def report(self, report: str):
        if self.node.report is not None:
            raise ValueError(f"Node {self.node.id} already has a report: {self.node.report}. Cannot update with {report}.")
        self.node.report = report
        SwarmNode.replace(self.node.id, self.node)
    
    def update_termination_policy(self, termination_policy: str, termination_handler: str = None):
        """
        Updates the termination policy of the node. If the termination policy is set to custom_termination_handler, 
        the termination handler will be set to the function name passed in the termination_handler parameter.
        """
        self.node.termination_policy = termination_policy
        SwarmNode.replace(self.node.id, self.node)
        if termination_policy == "custom_termination_handler":
            self.replace_execution_memory(execution_memory={"__termination_handler__": termination_handler})
    
    def add_value_to_execution_memory(self, attribute: str, value: Any):
        self.node.execution_memory[attribute] = value
        SwarmNode.replace(self.node.id, self.node)
    
    def remove_value_from_execution_memory(self, attribute: str):
        del self.node.execution_memory[attribute]
        SwarmNode.replace(self.node.id, self.node)

    def replace_execution_memory(self, execution_memory: Dict[str, Any]):
        self.node.execution_memory = execution_memory
        SwarmNode.replace(self.node.id, self.node)

    def clear_execution_memory(self):
        self.node.execution_memory = {}
        SwarmNode.replace(self.node.id, self.node)

    @staticmethod
    def custom_termination_handler(func: Callable):
        """
            This decorator is used to mark a function as a custom termination handler.

            Functions marked with this decorator should accept two parameters:
                - terminator_id: The id of the terminator node that this node spawned
                - context: Context persisted from spawning the terminator node

            This allows us to easily spawn new nodes, and then respond to the termination of those nodes.
        """
        def wrapper(self, **kwargs):
            terminator_id = kwargs.pop("terminator_id", None)
            context = kwargs.pop("context", None)
            
            if not terminator_id:
                raise ValueError(f"terminator_id is a required parameter for custom_termination_handler. Error in {self.node.id} at function {func.__name__}")
            if not context:
                raise ValueError(f"context is a required parameter for custom_termination_handler. Error in {self.node.id} at function {func.__name__}")

            return func(self, terminator_id, context)
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
                models_module = ActionMetadata.get_action_module(self.node.type)
                instructor_model = getattr(models_module, instructor_model_name)
                completion = instructor_model.model_validate(completion)

            if context:
                return func(self, completion, context)
            else:
                return func(self, completion)
        return wrapper

    @staticmethod
    def ask_questions_wrapper(func: Callable):
        """        
        The wrapped function needs to accept:
            - message: str
            - context: Optional[Dict[str, Any]]
        
        The message should be a directive, decision or task. This wrapper will force an additional step,
        to ask questions, before the wrapped function is called. This is to ensure that the LLM has
        full context before performing any action. Questions are answered by the oracle.

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
        - Saves original message in operational context
        - Returns a Blocking Operation of type "ask_questions" with the message and context.

        2. Accessing the oracle:
            Expected parameters: (completion: Any, context: Dict[str, Any])
        - Checks if the `questions` field in the completion is None.
        - If the `questions` field in the completion is None, call the wrapped function.
        - If not None, spawns an oracle node to answer the questions and set 
        this node's termination handler to the wrapped function so that we can
        handle the oracle's response.

        3. Handling the oracle's completion:
            Expected parameters: (terminator_id: str, context: Dict[str, Any])
        - Appends the report from the oracle node to the message in context.
        - Returns a Blocking Operation of type "ask_questions" with the message and context.
 
        This process repeats until the LLM has no more questions.
        """
        @wraps(func)
        def wrapper(self, **kwargs):
            message = kwargs.pop("message", None)
            context = kwargs.pop("context", None)
            completion = kwargs.get("completion", None)
            if type(completion) is not dict and completion: completion = completion.model_dump()
            terminator_id = kwargs.get("terminator_id", None)
            
            if message: # Stage 1
                if context is None: context = {}
                context["__message__"] = message
                return BlockingOperation(
                    node_id=self.node.id,
                    blocking_type="ask_questions",
                    args={"message": message},
                    context=context,
                    next_function_to_call=func.__name__
                )
            elif completion: # Stage 2
                if completion["questions"]:
                    self.update_termination_policy(termination_policy="custom_termination_handler", termination_handler=func.__name__)
                    return SpawnOperation(
                        parent_id=self.node.id,
                        action_id="specific/oracle",
                        message={
                            "questions": completion["questions"], 
                            "context": completion["context"]
                        },
                        context=context
                    )
                else:
                    message = context.pop("__message__")
                    if context: return func(self, message, context)
                    else: return func(self, message)
            elif terminator_id: # Stage 3
                terminator_node = BaseNode.read(terminator_id)
                oracle_report = terminator_node.report
                context["__message__"] += f"\n\n{oracle_report}"
                return BlockingOperation(
                    node_id=self.node.id,
                    blocking_type="ask_questions",
                    args={"message": message},
                    context=context,
                    next_function_to_call=func.__name__
                )
            else:
                raise ValueError(f"ask_questions wrapper called with invalid parameters: {kwargs}")
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
#             #     parent_id=self.node.id,
#             #     node_embryo=NodeEmbryo(
#             #         action_id="swarmstar/actions/swarmstar/handle_failure",
#             #         message=error_message,
#             #         context={'error_details': error_details}
#             #     )
#             # )
    
#     return wrapper