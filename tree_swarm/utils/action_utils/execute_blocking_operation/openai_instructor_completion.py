'''
This blocking operation will call openai with instructor. It expects 
a pydantic model and a list of messages, and will return a BlockingOperation
which will call the next_function_to_call of the node's action with the completion
and context.
'''
from __future__ import annotations
from typing import TYPE_CHECKING

from tree_swarm.utils.ai.openai_instructor import completion
from tree_swarm.swarm.types import BlockingOperation

if TYPE_CHECKING:
    from tree_swarm.swarm.types import Swarm

def execute_blocking_operation(swarm: Swarm, blocking_operation: BlockingOperation):
    messages = blocking_operation.args['messages']
    instructor_model = blocking_operation.args['instructor_model']
    
    response = completion(messages=messages, openai_key=swarm.configs.openai_key, instructor_model=instructor_model)
    
    return BlockingOperation(
        lifecycle_command=blocking_operation.lifecycle_command,
        node_id=blocking_operation.node_id,
        type='internal_action',
        args={
            "completion": response
        },
        context=blocking_operation.context,
        next_function_to_call=blocking_operation.next_function_to_call
    )
