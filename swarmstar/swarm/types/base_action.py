'''
This module contains the base class for all actions.
This base class: 

    - Provides some common methods that actions use.
    - Provides a metaclass to apply an error handling decorator to all methods of the action.

'''
from abc import ABCMeta, abstractmethod, ABC
from functools import wraps
import traceback

from typing import List, Dict

from swarmstar.swarm.types import SwarmConfig, SwarmOperation, SwarmNode, SwarmState, FailureOperation


def error_handling_decorator(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            self = args[0]  # Assuming the first argument is always 'self' for instance methods
            # Capturing the full traceback
            tb_str = traceback.format_exc()
            # Optionally, you can include function parameters in the report
            params_str = f"Parameters: args={args[1:]}, kwargs={kwargs}"
            report = f"Error in {func.__name__}:\n{str(e)}\n\n{tb_str}\n\n{params_str}"
            return FailureOperation(
                node_id=self.node.id,
                report=report,
            )
    return wrapper

class ErrorHandlingMeta(ABCMeta):
    def __new__(cls, name, bases, dct):
        new_cls = super().__new__(cls, name, bases, dct)
        for attr_name, attr_value in dct.items():
            if callable(attr_value):
                setattr(new_cls, attr_name, error_handling_decorator(attr_value))
        return new_cls

class BaseAction(metaclass=ErrorHandlingMeta):
    '''
    All actions should subclass this class.
    '''    
    def __init__(self, swarm: SwarmConfig, node: SwarmNode):
        self.swarm = swarm
        self.node = node
    
    @abstractmethod
    def main(self, **kwargs) -> SwarmOperation:
        pass
    
    def overwrite_report(self, report: str):
        self.node.report = report
        swarm_state = SwarmState(swarm=self.swarm)
        swarm_state.update_node(self.node)
        
    def append_report(self, report: str):
        self.node.report += f"\n\n{report}"
        swarm_state = SwarmState(swarm=self.swarm)
        swarm_state.update_node(self.node)
        
    def update_termination_policy(self, termination_policy: str):
        self.node.termination_policy = termination_policy
        swarm_state = SwarmState(swarm=self.swarm)
        swarm_state.update_node(self.node)
    
    def handle_failure(func):
        def wrapper(self, *args, **kwargs):
            # Now 'self' is explicitly available here, and you can use it.
            print(f"Method {func.__name__} of {self.__class__.__name__}")
            return func(self, *args, **kwargs)
        return wrapper
