'''
This blocking operation will call openai with instructor. It expects 
a pydantic model and a list of messages, and will return a BlockingOperation
which will call the next_function_to_call of the node's action with the completion
and context.
'''
from __future__ import annotations
from typing import TYPE_CHECKING, List, Dict
from importlib import import_module

from swarmstar.utils.ai.openai_instructor import completion
from swarmstar.swarm.types import BlockingOperation

if TYPE_CHECKING:
    from swarmstar.swarm.types import SwarmConfig
    
# This is the expected format of the args param for this blocking operation
def expected_args(BaseModel):
    messages: List[Dict[str, str]]             # This should be a list of dictionaries with the keys 'role' and 'content'
    instructor_model_name: str                 # This should point to a pydnatic model in the swarmstar.utils.ai.openai_instructor.models module

def execute_blocking_operation(swarm: SwarmConfig, blocking_operation: BlockingOperation) -> BlockingOperation:
    messages = blocking_operation.args['messages']
    instructor_model_name = blocking_operation.args['instructor_model_name']
    
    models_module = import_module('swarmstar.utils.swarm_utils.blocking_operations.instructor.pydantic_models')
    instructor_model = getattr(models_module, instructor_model_name)
    
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
