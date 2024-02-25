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

from swarmstar.swarm.types.swarm_config import SwarmConfig
from swarmstar.swarm.types.swarm_nodes import SwarmNode
from swarmstar.swarm.types.swarm_operations import SwarmOperation
from swarmstar.swarm.types.swarm_state import SwarmState


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
            params_str = f"node_id: {self.node.node_id}\nParams: {kwargs}"

            error_message = (
                f"Error in {func.__name__}:\n{str(e)}\n\n{tb_str}\n\n{params_str}"
            )
            raise Exception(error_message)

            # return FailureOperation(
            #     node_id=self.node.node_id,
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

    def __init__(self, swarm: SwarmConfig, node: SwarmNode):
        self.swarm = swarm
        self.node = node

    @abstractmethod
    def main(self, **kwargs) -> SwarmOperation:
        pass

    def add_journal_entry(self, journal_entry: Dict[str, Any]):
        self.node.journal.append(journal_entry)
        swarm_state = SwarmState(swarm=self.swarm)
        swarm_state.update_state(self.node)

    def add_developer_log(self, developer_log: Dict[str, Any]):
        self.node.developer_logs.append(developer_log)
        swarm_state = SwarmState(swarm=self.swarm)
        swarm_state.update_state(self.node)

    def update_termination_policy(self, termination_policy: str):
        self.node.termination_policy = termination_policy
        swarm_state = SwarmState(swarm=self.swarm)
        swarm_state.update_state(self.node)
