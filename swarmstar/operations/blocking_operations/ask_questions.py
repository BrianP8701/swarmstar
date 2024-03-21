"""
This blocking operation will call openai with instructor. It expects 
a pydantic model and a list of messages, and will return a BlockingOperation
which will call the next_function_to_call of the node's action with the completion
and context.
"""
from swarmstar.models import BlockingOperation, ActionOperation, BaseNode
from swarmstar.utils.ai import Instructor
from swarmstar.utils.ai.instructor_models import AskQuestions
from swarmstar.utils.ai.prompts import ASK_QUESTIONS_INSTRUCTIONS

instructor = Instructor()

async def blocking(blocking_operation: BlockingOperation) -> BlockingOperation:
    node = BaseNode.get(blocking_operation.node_id)

    message = blocking_operation.args["message"]

    response = await instructor.completion(
        messages=[{
            "role": "system",
            "content": ASK_QUESTIONS_INSTRUCTIONS + "\n\n" + message
        }],
        instructor_model=AskQuestions
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
