"""
This blocking operation will call openai with instructor. It expects 
a pydantic model and a list of messages, and will return a BlockingOperation
which will call the next_function_to_call of the node's action with the completion
and context.
"""
from importlib import import_module

from swarmstar.models import BlockingOperation, ActionOperation, BaseNode, ActionMetadata
from swarmstar.utils.ai import Instructor
from swarmstar.utils.ai.instructor_models import QuestionWrapper
from swarmstar.utils.ai.prompts import ORACLE_ACCESS_INSTRUCTIONS

instructor = Instructor()

async def blocking(blocking_operation: BlockingOperation) -> BlockingOperation:
    node = BaseNode.get(blocking_operation.node_id)

    message = blocking_operation.args["message"]
    instructor_model_name = blocking_operation.args["instructor_model_name"]
    module = ActionMetadata.get_action_module(node.type)

    instructor_model = getattr(module, instructor_model_name)
    
    print("\n\n\n\n\n")
    print(instructor_model)
    print(type(instructor_model))
    print("\n\n\n\n\n")    
    

    if blocking_operation.context.get("__oracle_access__", False):
        instructor_model = type(instructor_model_name, (QuestionWrapper, instructor_model), {})
        message = f"{message}\n\n{ORACLE_ACCESS_INSTRUCTIONS}"

    print("\n\n\n\n\n")
    print(message)
    print(type(message))
    print("\n\n")
    print(instructor_model)
    print(type(instructor_model))
    print("\n\n\n\n\n")



    response = await instructor.completion(
        messages={
            "role": "system",
            "content": message
        },
        instructor_model=instructor_model
    )
    
    log_index_key = blocking_operation.context.get("log_index_key", None)

    node.log({
        "role": "swarmstar",
        "content": message
    }, log_index_key)
    node.log({
        "role": "ai",
        "content": response.model_dump_json(indent=2)
    }, log_index_key)

    return ActionOperation(
        node_id=blocking_operation.node_id,
        function_to_call=blocking_operation.next_function_to_call,
        args={
            "completion": response, 
            "context": blocking_operation.context
        },
    )
