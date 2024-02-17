'''
This blocking operation will call openai with instructor. It expects 
a pydantic model and a list of messages, and will return a BlockingOperation
which will call the next_function_to_call of the node's action with the completion
and context.
'''
from __future__ import annotations
from typing import TYPE_CHECKING

from swarm_star.utils.ai.openai_instructor import completion
from swarm_star.swarm.types import BlockingOperation

if TYPE_CHECKING:
    from swarm_star.swarm.types import SwarmConfig

def execute_blocking_operation(swarm: SwarmConfig, blocking_operation: BlockingOperation):
    messages = blocking_operation.args['messages']
    instructor_model = blocking_operation.args['instructor_model']
    
    response = completion(messages=messages, openai_key=swarm.openai_key, instructor_model=instructor_model)
    
    return BlockingOperation(
        operation_type=blocking_operation.operation_type,
        node_id=blocking_operation.node_id,
        blocking_type='internal_action',
        args={
            "completion": response
        },
        context=blocking_operation.context,
        next_function_to_call=blocking_operation.next_function_to_call
    )
