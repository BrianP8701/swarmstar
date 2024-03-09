# pytest tests/unit_tests/test_actions/test_decompose_directive.py
import pytest

from swarmstar.core import execute_swarmstar_operation
from swarmstar.types import NodeEmbryo, SpawnOperation
from tests.utils.get_local_swarm_config import get_swarm_config


@pytest.mark.unit_test_actions
@pytest.mark.requires_openai
def test_decompose_directive():
    swarm = get_swarm_config("swarmstar_unit_tests")
    spawn_decompose_directive_node = SpawnOperation(
        node_embryo=NodeEmbryo(
            action_id="swarmstar/actions/reasoning/decompose_directive",
            message='Create and add a web browsing action to the swarm\'s action space. The action name should be "browse_web".',
        )
    )

    next_swarm_operation = execute_swarmstar_operation(swarm, spawn_decompose_directive_node)
    while next_swarm_operation[0].operation_type != "spawn":
        next_swarm_operation = execute_swarmstar_operation(swarm, next_swarm_operation[0])

    assert next_swarm_operation[0].operation_type == "spawn"
    assert (
        next_swarm_operation[0].node_embryo.action_id
        == "swarmstar/actions/reasoning/route_action"
    )
