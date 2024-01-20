import sys
import pytest
sys.path.insert(0, '/Users/brianprzezdziecki/Code/Agent_Swarm_Experiments')

from swarm.utils.actions.executor import execute_node
from swarm.core.node import Node

import asyncio

@pytest.mark.unit_test_actions
async def test_manager():
    node = Node(id=5, type='manager', data={'directive': "We need to see the code for the Swarm class."})
    result = await execute_node(node)
    print(result)

# Run the main function
asyncio.run(test_manager())