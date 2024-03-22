"""
This blocking operation will call openai with instructor. It expects 
a pydantic model and a list of messages, and will return a BlockingOperation
which will call the next_function_to_call of the node's action with the completion
and context.
"""
from swarmstar.models import BlockingOperation, ActionOperation, BaseNode, ActionMetadata
from swarmstar.utils.ai import Instructor

instructor = Instructor()

async def blocking(blocking_operation: BlockingOperation) -> BlockingOperation:
    node = BaseNode.read(blocking_operation.node_id)

    message = blocking_operation.args["message"]
    instructor_model_name = blocking_operation.args["instructor_model_name"]
    module = ActionMetadata.get_action_module(node.type)

    instructor_model = getattr(module, instructor_model_name)

    response = await instructor.completion(
        messages=[{
            "role": "system",
            "content": message
        }],
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
