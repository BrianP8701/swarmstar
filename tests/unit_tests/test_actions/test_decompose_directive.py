# pytest tests/unit_tests/test_actions/test_decompose_directive.py
import pytest

from swarmstar.swarm.core import execute_swarm_operation
from swarmstar.swarm.types import SpawnOperation, NodeEmbryo, SwarmConfig, LocalConfig
from swarmstar.utils.misc.uuid import generate_uuid

from tests.utils.get_local_swarm_config import get_swarm_config
from tests.utils.upload_results import create_result_file, add_swarm_operation

@pytest.mark.unit_test_actions
def test_decompose_directive():
    results_file = create_result_file()
    swarm = get_swarm_config('swarmstar_unit_tests')
    spawn_decompose_directive_node = SpawnOperation(
        operation_type='spawn',
        node_embryo=NodeEmbryo(
            action_id='swarmstar/actions/reasoning/decompose_directive',
            message='Create and add a web browsing action to the swarm\'s action space. The action name should be "browse_web".'
        )
    )
    
    next_swarm_operation = execute_swarm_operation(swarm, spawn_decompose_directive_node)
    add_swarm_operation(results_file, next_swarm_operation[0])
    while next_swarm_operation[0].operation_type != 'spawn':
        next_swarm_operation = execute_swarm_operation(swarm, next_swarm_operation[0])
        for swarm_operation in next_swarm_operation:
            add_swarm_operation(results_file, swarm_operation)
            
    for swarm_operation in next_swarm_operation:
        add_swarm_operation(results_file, swarm_operation)
    

test_decompose_directive()