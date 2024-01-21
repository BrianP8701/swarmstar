import sys
import pytest
sys.path.insert(0, '/Users/brianprzezdziecki/Code/Agent_Swarm_Experiments')

from swarm.core.swarm import Swarm

import asyncio

@pytest.mark.unit_test_actions
async def test_action_router():
    swarm = Swarm()
    directive = 'write a script that prints "Hello World"'
    swarm.load_directive(directive)
    await swarm.run()
    

# Run the main function
asyncio.run(test_action_router())