import os
import sys
import pytest
sys.path.insert(0, '/Users/brianprzezdziecki/Code/Agent_Swarm_Experiments')

from swarm.utils.actions.executor import execute
from swarm.core.node import Node

import asyncio

async def main():
    node = Node(id=5, type='action_router', data={'directive': "Write a python script that prints 'Hello World'"})
    result = await execute(node)
    print('hey')
    print(result)

# Run the main function
asyncio.run(main())