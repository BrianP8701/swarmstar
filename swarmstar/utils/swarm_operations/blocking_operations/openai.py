"""
This blocking operation will call openai with instructor. It expects 
a pydantic model and a list of messages, and will return a BlockingOperation
which will call the next_function_to_call of the node's action with the completion
and context.
"""
from importlib import import_module
from typing import Dict, List

from pydantic import BaseModel

from swarmstar.models import BlockingOperation, ActionOperation
from swarmstar.utils.ai import OpenAI

openai = OpenAI()

class expected_args(BaseModel):
    messages: List[
        Dict[str, str]
    ]  # This should be a list of dictionaries with the keys 'role' and 'content'


async def blocking(blocking_operation: BlockingOperation) -> BlockingOperation:
    messages = blocking_operation.args["messages"]

    response = await openai.completion(
        messages=messages,
    )
    
    return ActionOperation(
        node_id=blocking_operation.node_id,
        function_to_call=blocking_operation.next_function_to_call,
        args={**{"completion": response}, **blocking_operation.context},
    )
