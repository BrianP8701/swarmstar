# pytest tests/unit_tests/test_actions/test_ask_user_questions.py
import pytest

from swarmstar.swarm.core import swarmstar_god
from swarmstar.swarm.types import BlockingOperation, NodeEmbryo, SpawnOperation
from tests.utils.get_local_swarm_config import get_swarm_config


@pytest.mark.unit_test_actions
@pytest.mark.requires_openai
def test_ask_user_questions():
    swarm = get_swarm_config("swarmstar_unit_tests")
    spawn_user_question_asker_node = SpawnOperation(
        node_embryo=NodeEmbryo(
            action_id="swarmstar/actions/communication/ask_user_questions",
            message="Just ask the user what his favorite color and memory is. This is a test.",
        )
    )
    next_swarm_operation = swarmstar_god(swarm, spawn_user_question_asker_node)

    while (
        next_swarm_operation[0].operation_type != "spawn"
        and next_swarm_operation[0].operation_type != "terminate"
    ):
        if (
            next_swarm_operation[0].blocking_type == "instructor_completion"
            or next_swarm_operation[0].blocking_type == "internal_action"
        ):
            next_swarm_operation = swarmstar_god(swarm, next_swarm_operation[0])
        elif next_swarm_operation[0].blocking_type == "send_user_message":
            ai_message = next_swarm_operation[0].args["message"]
            print(f"AI: {ai_message}\nUser: ")
            user_input = input()
            next_swarm_operation = [
                BlockingOperation(
                    node_id=next_swarm_operation[0].node_id,
                    blocking_type="internal_action",
                    args={"user_response": user_input},
                    context=next_swarm_operation[0].context,
                    next_function_to_call=next_swarm_operation[0].next_function_to_call,
                )
            ]
        else:
            raise ValueError(
                f"Unexpected blocking type: {next_swarm_operation[0].blocking_type}"
            )

    assert next_swarm_operation[0].operation_type == "terminate"
