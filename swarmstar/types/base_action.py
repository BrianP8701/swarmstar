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
from typing import Any, Dict

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
    def main(self, **kwargs) -> SwarmOperation:
        pass

    def log(self, log_dict: Dict[str, Any]):
        """
        log_dict: {"role": "swarmstar, system, ai or user", "message": "Some message"}
        """
        self.node.developer_logs.append(log_dict)
        update_swarm_node(self.swarm, self.node)

    def update_termination_policy(self, termination_policy: str):
        self.node.termination_policy = termination_policy
        update_swarm_node(self.swarm, self.node)
