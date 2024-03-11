"""file for quick tests. nothing to see here."""
import pymongo
from pymongo import MongoClient
from typing import Any, Dict, List, Tuple, get_origin, get_args
from tests.test_config import SWARMSTAR_UNIT_TESTS_MONGODB_DB_NAME, MONGODB_URI

from swarmstar.types import SwarmConfig, SwarmNode, SpawnOperation, BlockingOperation
from swarmstar.utils.swarmstar_space import get_swarm_node, get_action_metadata, get_swarm_config
from swarmstar.utils.data import get_kv, get_internal_action_metadata

import traceback
from abc import ABCMeta, abstractmethod
from functools import wraps
from typing import Any, Dict, List, Callable, get_type_hints
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


class TestAction(BaseAction):
    def main(self) -> [SwarmOperation, List[SwarmOperation]]:
        pass

    @BaseAction.termination_handler
    def analyze_branch_question_answers(self, terminator_node_id: str, context: Dict[str, Any]) -> List[SwarmOperation]:
        print("it worked")

swarm_config = get_swarm_config(MONGODB_URI, SWARMSTAR_UNIT_TESTS_MONGODB_DB_NAME, "default_config")
test_node = SwarmNode(
    name="test",
    action_id="test",
    message="test",
    termination_policy="simple"

)
test = TestAction(swarm_config, test_node)

test.analyze_branch_question_answers("test", {})