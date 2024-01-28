import json
from typing import List

from aga_swarm.swarm.types import *
from aga_swarm.swarm.swarm_lifecycle import spawn_node, swarm_master
from aga_swarm.swarm.swarm_utils import get_action_name
from aga_swarm.utils.uuid import generate_uuid

with open('/Users/brianprzezdziecki/Code/autonomous-general-agent-swarm/z/test_swarm_instance/swarm_id.json', 'r') as f:
    swarm_id_json = json.loads(f.read())

swarm_id = SwarmID.model_validate_json(swarm_id_json)

directive = '''Go through the data folder in actions. look at all the actions inside, 
which consist of mac platform operations. in addition to those add corresponding 
operations for windows, linux file system,  azure gcp and aws blob storage'''

swarm_command = SwarmCommand(
    action_id='aga_swarm/actions/reasoning/manager/manager.py',
    params={
        'directive': directive,
        'swarm_id': swarm_id
    }
)

# manager_node = spawn_node(swarm_id, swarm_command, None)

node = SwarmNode(
    node_id=generate_uuid(get_action_name(swarm_id, swarm_command.action_id)),
    parent_id=None,
    children_ids=[],
    swarm_command=swarm_command,
    alive=True
)

nodes: List[SwarmNode] = swarm_master(swarm_id, node)
print('\n\n\n')
for node in nodes:
    print(node.swarm_command.params['directive'])
print('\n\n\n')