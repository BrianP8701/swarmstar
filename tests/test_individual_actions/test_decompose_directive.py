import os
import pytest
from typing import List

from tree_swarm.swarm.core import execute_blocking_operation, execute_node, spawn_node
from tree_swarm.swarm.setup import setup_swarm_space
from tree_swarm.swarm.types import SwarmCommand, BlockingOperation

def check_path_exists(base_path: str, suffix: str = '') -> str:
    i = 0
    while True:
        path = f'{base_path}{suffix}{i}'
        if not os.path.exists(path):
            return path
        i += 1

def test_decompose_directive():
    openai_key = os.environ.get('OPENAI_API_KEY')
    path = check_path_exists('/Users/brianprzezdziecki/Code/autonomous-general-agent-swarm/my_swarms/test_2_12_24__', '_')
    swarm = setup_swarm_space(openai_key, 'blank for now', path, 'mac')
    message = 'We need to add a thing to the swarm interface so in the agent chat section, when the agent outputs codeblock we can actually see like a nice code block in the interface. like black background, some colored text, like a code editor. You know, like when chatgpt generates code they actually make a code block for visual.... cuz its visually appealing.'
    node = spawn_node(
        swarm,
        SwarmCommand(
            action_id='tree_swarm/actions/reasoning/decompose_directive',
            message=message
        )
    )
    swarm_master_command = [node]
    while swarm_master_command != None:
        if type(swarm_master_command) == BlockingOperation:
            swarm_master_command = execute_blocking_operation(swarm, swarm_master_command)
        elif type(swarm_master_command) == list:
            for node in swarm_master_command:
                swarm_master_command = execute_node(swarm, node)
        else:
            raise ValueError(f"Unexpected output type: {type(swarm_master_command)}")
        
    
test_decompose_directive()
    
