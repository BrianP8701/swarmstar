from swarmstar import execute_swarmstar_operation, spawn_swarm
from swarmstar.utils.swarmstar_space.swarm_config import get_swarm_config, add_swarm_config
from swarmstar.utils.swarmstar_space.general import spawn_swarmstar_space, delete_swarmstar_space
from tests.test_config import SWARMSTAR_UNIT_TESTS_MONGODB_DB_NAME, MONGODB_URI
from tests.utils.save_results import save_swarm_operation_info, find_next_available_results_file, find_next_available_folder

def test_create_web_app():
    try:
        goal = (
            'I want you to create a web app with 3 sections:\n'
            '1. A section where you can enter your goal and press spawn\n'
            '2. A section where you can talk to multiple agents at once\n'
            '3. A section where you can visualize the swarm\'s state'
            '4. A section where you can visualize the swarm\'s history'
        )
        swarm_config = get_swarm_config(MONGODB_URI, SWARMSTAR_UNIT_TESTS_MONGODB_DB_NAME, "default_config")
        swarm_config.id = 'temp'
        swarm_config.root_path = find_next_available_folder()
        add_swarm_config(swarm_config)
        
        results_file_path = find_next_available_results_file('tests/results/')
        
        root_spawn_operation = spawn_swarm(swarm_config, goal)
        save_swarm_operation_info(swarm_config, root_spawn_operation, results_file_path)
        operations_to_execute = execute_swarmstar_operation(swarm_config, root_spawn_operation)

        while True:
            next_operations_to_execute = []
            for operation in operations_to_execute:
                print('\n\n\n\n\n')
                print(operation)
                print('\n\n\n\n\n')
                save_swarm_operation_info(swarm_config, operation, results_file_path)
                next_operations = execute_swarmstar_operation(swarm_config, operation)
                next_operations_to_execute.extend(next_operations)
            pause = input('Press enter to continue')
            operations_to_execute = next_operations_to_execute
            if not operations_to_execute:
                break
        
        delete_swarmstar_space(swarm_config)
    except Exception as e:
        delete_swarmstar_space(swarm_config)
        raise(e)
    
    


test_create_web_app()
