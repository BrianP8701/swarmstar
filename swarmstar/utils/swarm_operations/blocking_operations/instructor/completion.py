"""
This blocking operation will call openai with instructor. It expects 
a pydantic model and a list of messages, and will return a BlockingOperation
which will call the next_function_to_call of the node's action with the completion
and context.
"""
from importlib import import_module
from typing import Dict, List

from pydantic import BaseModel

from swarmstar.types import BlockingOperation, ActionOperation
from swarmstar.utils.ai.openai_instructor import completion
from swarmstar.types import SwarmConfig


class expected_args(BaseModel):
    messages: List[
        Dict[str, str]
    ]  # This should be a list of dictionaries with the keys 'role' and 'content'
    instructor_model_name: str  # This should point to a pydnatic model in the swarmstar.utils.ai.openai_instructor.models module


async def blocking(
    swarm: SwarmConfig, blocking_operation: BlockingOperation
) -> BlockingOperation:
    messages = blocking_operation.args["messages"]
    instructor_model_name = blocking_operation.context["instructor_model_name"]

    models_module = import_module(
        "swarmstar.utils.swarm_operations.blocking_operations.instructor.pydantic_models"
    )
    instructor_model = getattr(models_module, instructor_model_name)

    response = await completion(
        messages=messages,
        openai_key=swarm.openai_key,
        instructor_model=instructor_model
    )
    
    return ActionOperation(
        node_id=blocking_operation.node_id,
        function_to_call=blocking_operation.next_function_to_call,
        args={**{"completion": response}, **blocking_operation.context},
    )
