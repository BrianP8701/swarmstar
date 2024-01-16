import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from swarm.core.executor import execute
from swarm.core.node import Node

import asyncio

async def main():
    node = Node(id=5, type='action_router', data={'directive': "Write a python script that prints 'Hello World'"})
    result = await execute(node)
    print('hey')
    print(result)

# Run the main function
asyncio.run(main())