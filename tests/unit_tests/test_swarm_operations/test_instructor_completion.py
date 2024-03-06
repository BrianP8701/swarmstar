import pytest

from swarmstar.swarm.core import execute_swarmstar_operation
from swarmstar.types import (
    BlockingOperation,
)
from tests.test_config import SWARMSTAR_UNIT_TESTS_MONGODB_DB_NAME
from tests.utils.get_local_swarm_config import get_swarm_config


@pytest.mark.unit_test_operations
@pytest.mark.requires_openai
def test_instructor_completion():
    swarm = get_swarm_config(SWARMSTAR_UNIT_TESTS_MONGODB_DB_NAME)

    instructor_completion_operation = BlockingOperation(
        node_id="NA",
        blocking_type="instructor_completion",
        args={
            "messages": [
                {
                    "role": "system",
                    "content": "Just output 2 short random directives. This is testing.",
                }
            ],
            "instructor_model_name": "DecomposeDirectiveModel",
        },
        next_function_to_call="NA",
    )

    output = execute_swarmstar_operation(swarm, instructor_completion_operation)

    assert output.operation_type == "blocking"
    assert output.node_id == "NA"
    assert output.blocking_type == "internal_action"
