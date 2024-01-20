import sys
import pytest
sys.path.insert(0, '/Users/brianprzezdziecki/Code/Agent_Swarm_Experiments')

from swarm.utils.actions.executor import execute_node
from swarm.core.node import Node

import asyncio

# @pytest.mark.temp
async def main():
    node = Node(id=5, type='code/python_coder', data={'directive': "Write a python script that prints 'Hello World'"})
    result = await execute_node(node)
    print('hey')
    print(result)

# Run the main function
asyncio.run(main())
