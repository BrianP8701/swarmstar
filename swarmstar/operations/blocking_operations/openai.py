"""
This blocking operation will call openai with instructor. It expects 
a pydantic model and a list of messages, and will return a BlockingOperation
which will call the next_function_to_call of the node's action with the completion
and context.
"""
from swarmstar.models import BlockingOperation, ActionOperation, BaseNode
from swarmstar.utils.ai import OpenAI

openai = OpenAI()

async def blocking(blocking_operation: BlockingOperation) -> BlockingOperation:
    message = blocking_operation.args["message"]

    response = await openai.completion(
        messages={
            "role": "system",
            "content": message
        }
    )
    
    node = BaseNode.read(blocking_operation.node_id)
    log_index_key = blocking_operation.context.get("log_index_key", None)

    node.log({
        "role": "swarmstar",
        "content": message
    }, log_index_key)
    node.log({
        "role": "ai",
        "content": response
    }, log_index_key)
    
    return ActionOperation(
        node_id=blocking_operation.node_id,
        function_to_call=blocking_operation.next_function_to_call,
        args={**{"completion": response}, **blocking_operation.context},
    )
