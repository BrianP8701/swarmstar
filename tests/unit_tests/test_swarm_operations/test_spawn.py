import pytest

from swarmstar.swarm.core import swarmstar_god
from swarmstar.swarm.types import SpawnOperation, NodeEmbryo, SwarmState

from tests.utils.get_local_swarm_config import get_swarm_config
from tests.test_config import SWARMSTAR_UNIT_TESTS_MONGODB_DB_NAME

@pytest.mark.unit_test_operations
def test_spawn_operation():
    swarm = get_swarm_config(SWARMSTAR_UNIT_TESTS_MONGODB_DB_NAME)
    
    spawn_operation = SpawnOperation(
        operation_type='spawn',
        node_embryo=NodeEmbryo(
            action_id='swarmstar/actions/reasoning/decompose_directive',
            message='Create and add a web browsing action to the swarm\'s action space. The action name should be "browse_web".'
        )
    )
    
    next_swarm_operation = swarmstar_god(swarm, spawn_operation)[0]
    
    swarm_state = SwarmState(swarm=swarm)
    spawned_node_id = next_swarm_operation.node_id
    node = swarm_state[spawned_node_id]
    assert node.node_id == spawned_node_id
    assert node.alive == True
    assert node.action_id == 'swarmstar/actions/reasoning/decompose_directive'
    assert node.message == 'Create and add a web browsing action to the swarm\'s action space. The action name should be "browse_web"'
