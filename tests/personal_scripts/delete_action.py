from aga_swarm.utils.action_space_utils import delete_action_space_node
from aga_swarm.swarm.types import *
from aga_swarm.utils.swarm_utils import get_action_space_metadata
import json

with open('/Users/brianprzezdziecki/Code/autonomous-general-agent-swarm/z/gratamatta/swarm_id.json', 'r') as f:
    swarm_id = f.read()
    
# Turn json string into dict
swarm_id = json.loads(swarm_id)

# Turn dict into SwarmID object
swarm_id = SwarmID(**swarm_id)

delete_action_space_node('aga_swarm/actions/swarm', swarm_id)
