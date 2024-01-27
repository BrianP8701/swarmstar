import json

from aga_swarm.swarm.types import SwarmID, SwarmCommand
# from aga_swarm.swarm.swarm_lifecycle import spawn_node, swarm_master

with open('/Users/brianprzezdziecki/Code/autonomous-general-agent-swarm/z/test_swarm_instance/swarm_id.json', 'r') as f:
    swarm_id_json = json.loads(f.read())

swarm_id = SwarmID.model_validate_json(swarm_id_json)

print(type(swarm_id))

# directive = '''Go through the data folder in actions. look at all the actions inside, 
# which consist of mac platform operations. in addition to those add corresponding 
# operations for windows, linux file system,  azure gcp and aws blob storage'''

# swarm_command = SwarmCommand(
#     action_id='aga_swarm/actions/swarm/manager/manager.py',
#     params={
#         'directive': directive,
#         'swarm_id': swarm_id
#     }
# )

# manager_node = spawn_node(swarm_command, None)

# swarm_master(swarm_command)