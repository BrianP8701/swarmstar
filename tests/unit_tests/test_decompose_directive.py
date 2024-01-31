import json
from typing import List

from aga_swarm.swarm.types import *
from aga_swarm.swarm.swarm_lifecycle import _spawn_node, swarm_master
from aga_swarm.utils.swarm_utils import get_action_name
from aga_swarm.utils.uuid import generate_uuid

with open('z/gratamatta/swarm_id.json', 'r') as f:
    swarm_id_dict = json.loads(f.read())

swarm_id = SwarmID.model_validate(swarm_id_dict)

directive = '''Go through the data folder in actions. look at all the actions inside, 
which consist of mac platform operations. in addition to those add corresponding 
operations for windows, linux file system,  azure gcp and aws blob storage'''

swarm_command = SwarmCommand(
    action_id='aga_swarm/actions/reasoning/decompose_directive',
    params={
        'directive': directive,
        'swarm_id': swarm_id
    }
)

manager_node = _spawn_node(swarm_id, swarm_command, None)



nodes: List[SwarmNode] = swarm_master(swarm_id, manager_node)
print('\n\n\n')
for node in nodes:
    print(node.swarm_command.params['directive'])
print('\n\n\n')
