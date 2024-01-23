import sys
import pytest
sys.path.insert(0, '/Users/brianprzezdziecki/Code/Agent_Swarm_Experiments')

from swarm.core.swarm import Swarm
import asyncio

@pytest.mark.integration_tests
async def test_hello_world():
    swarm = Swarm()
    directive = 'Write a script that prints hello world'
    swarm.load_directive(directive)
    await swarm.run()
    
# Run the main function
asyncio.run(test_hello_world())