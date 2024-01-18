import sys
import pytest
sys.path.insert(0, '/Users/brianprzezdziecki/Code/Agent_Swarm_Experiments')

from swarm.utils.actions.executor import execute_node
from swarm.core.node import Node

import asyncio

# @pytest.mark.temp
async def main():
    node = Node(id=5, type='memory/memory_router', data={'data_id': "swarm_overview.md"})
    result = await execute_node(node)
    print(result)

# Run the main function
asyncio.run(main())