import asyncio

from swarmstar import execute_swarmstar_operation, spawn_swarm
from swarmstar.models import Swarmstar, SwarmConfig

async def test_create_web_app():
    try:
        goal = (
            'I want you to create a web app with 3 sections:\n'
            '1. A section where you can enter your goal and press spawn\n'
            '2. A section where you can talk to multiple agents at once\n'
            '3. A section where you can visualize the swarm\'s state'
            '4. A section where you can visualize the swarm\'s history'
        )
        swarm_config = SwarmConfig.get_swarm_config("default_config")
        swarm_config.id = 'temp'
        SwarmConfig.add_swarm_config(swarm_config)
        
        
        root_spawn_operation = spawn_swarm(swarm_config, goal)
        operations_to_execute = await execute_swarmstar_operation(swarm_config, root_spawn_operation)

        while True:
            next_operations_to_execute = []
            for operation in operations_to_execute:
                print('\n\n\n\n\n')
                print(operation)
                print('\n\n\n\n\n')
                next_operations = await execute_swarmstar_operation(swarm_config, operation)
                next_operations_to_execute.extend(next_operations)
            pause = input('Press enter to continue')
            operations_to_execute = next_operations_to_execute
            if not operations_to_execute:
                break
        
        Swarmstar.delete_swarmstar_space(swarm_config)
    except Exception as e:
        Swarmstar.delete_swarmstar_space(swarm_config)
        raise(e)


asyncio.run(test_create_web_app())
