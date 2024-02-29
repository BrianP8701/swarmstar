from swarmstar import Swarmstar
from tests.utils.get_local_swarm_config import get_swarm_config
from tests.test_config import SWARMSTAR_UNIT_TESTS_MONGODB_DB_NAME
from tests.utils.save_results import save_swarm_operation_info, find_next_available_results_file

def test_create_web_app():
    goal = (
        'I want you to create a web app with 3 sections:\n'
        '1. A section where you can enter your goal and press spawn\n'
        '2. A section where you can talk to multiple agents at once\n'
        '3. A section where you can visualize the swarm\'s state'
        '4. A section where you can visualize the swarm\'s history'
    )
    swarm = get_swarm_config(SWARMSTAR_UNIT_TESTS_MONGODB_DB_NAME)
    ss = Swarmstar(swarm)
    
    results_file_path = find_next_available_results_file('tests/results/')
    
    
    root_spawn_operation = ss.spawn_root(goal)
    save_swarm_operation_info(swarm, root_spawn_operation, results_file_path)
    operations_to_execute = ss.execute(root_spawn_operation)

    while True:
        next_operations_to_execute = []
        for operation in operations_to_execute:
            print('\n\n\n\n\n')
            print('operations to execute')
            print(operations_to_execute)
            print('\n\n\n\n\n')
            print(operation)
            print('\n\n\n\n\n')
            save_swarm_operation_info(swarm, operation, results_file_path)
            next_operations = ss.execute(operation)
            next_operations_to_execute.extend(next_operations)
        pause = input('Press enter to continue')
        operations_to_execute = next_operations_to_execute


test_create_web_app()
