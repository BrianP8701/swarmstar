# pytest tests/unit_tests/test_actions/test_route_action.py
import pytest

from swarmstar.core import execute_swarmstar_operation
from swarmstar.types import NodeEmbryo, SpawnOperation
from tests.utils.get_local_swarm_config import get_swarm_config


@pytest.mark.unit_test_actions
@pytest.mark.requires_openai
def test_route_action():
    swarm = get_swarm_config("swarmstar_unit_tests")
    spawn_route_node = SpawnOperation(
        node_embryo=NodeEmbryo(
            action_id="swarmstar/actions/reasoning/route_action",
            message='Just choose the decompose directive action. This is a test.".',
        )
    )

    next_swarm_operation = execute_swarmstar_operation(swarm, spawn_route_node)
    while next_swarm_operation[0].operation_type != "spawn":
        next_swarm_operation = execute_swarmstar_operation(swarm, next_swarm_operation[0])

    assert next_swarm_operation[0].operation_type == "spawn"
    assert (
        next_swarm_operation[0].node_embryo.action_id
        == "swarmstar/actions/reasoning/decompose_directive_action"
    )
