import sys
import pytest
sys.path.insert(0, '/Users/brianprzezdziecki/Code/Agent_Swarm_Experiments')

from swarm.utils.actions.executor import execute_node
from swarm.core.node import Node
from swarm.utils.memory.save_to_stage import stage_content

import asyncio

@pytest.mark.unit_test_actions
async def test_memory_router():
    metadata = {
        'description': 'this file contains an introductory overview of the swarm',
        'file_extension': 'md'
    }
    id = stage_content('blah blah blah', metadata, 'swarm_overview')

    node = Node(id=5, type='memory/memory_router', data={'data_id': id})
    result = await execute_node(node)
    assert result['action'] == 'terminate'

# Run the main function
asyncio.run(test_memory_router())