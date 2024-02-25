import os

from swarmstar.swarm.core import swarmstar_god
from swarmstar.swarm.types import NodeEmbryo, SpawnOperation, SwarmConfig
from swarmstar.swarm.setup import configure_swarm
from tests.utils.create_local_swarm_space import find_next_available_swarm_folder
from tests.utils.get_local_swarm_config import get_swarm_config
from tests.test_config import SWARMSTAR_UNIT_TESTS_MONGODB_DB_NAME
from tests.utils.save_results import save_dict_to_json_file, save_swarm_operation_info, find_next_available_results_file

def test_create_web_app():
    goal = (
        'I want you to create a web app with 3 sections:\n'
        '1. A section where you can enter your goal and press spawn\n'
        '2. A section where you can talk to multiple agents at once\n'
        '3. A section where you can visualize the swarm\'s state'
    )
    swarm = get_swarm_config(SWARMSTAR_UNIT_TESTS_MONGODB_DB_NAME)

    
    results_file_path = find_next_available_results_file('tests/results/')
    
    
    root_node_spawn = SpawnOperation(
        node_embryo=NodeEmbryo(
            action_id='swarmstar/actions/reasoning/decompose_directive',
            message=goal
        )
    )
    save_swarm_operation_info(swarm, root_node_spawn, results_file_path)
    operations_to_execute = swarmstar_god(swarm, root_node_spawn)

    while True:
        next_operations_to_execute = []
        for operation in operations_to_execute:
            save_swarm_operation_info(swarm, operation, results_file_path)
            next_operations = swarmstar_god(swarm, operation)
            next_operations_to_execute.extend(next_operations)
        pause = input('Press enter to continue')
        operations_to_execute = next_operations_to_execute


test_create_web_app()
