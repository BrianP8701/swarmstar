import json
from typing import List

from aga_swarm.swarm.types import *
from aga_swarm.swarm.swarm_lifecycle import _spawn_node, swarm_master
from aga_swarm.utils.uuid import generate_uuid

with open('z/gratamatta/swarm_config.json', 'r') as f:
    swarm_config_dict = json.loads(f.read())

swarm_config = SwarmConfig.model_validate(swarm_config_dict)

directive = '''Go through the data folder in actions. look at all the actions inside, 
which consist of mac platform operations. in addition to those add corresponding 
operations for windows, linux file system,  azure gcp and aws blob storage'''

swarm_command = SwarmCommand(
    action_id='aga_swarm/actions/reasoning/decompose_directive',
    params={
        'directive': directive,
        'swarm_config': swarm_config
    }
)

manager_node = _spawn_node(swarm_config, swarm_command, None)



nodes: List[SwarmNode] = swarm_master(swarm_config, manager_node)
print('\n\n\n')
for node in nodes:
    print(node.swarm_command.params['directive'])
print('\n\n\n')
