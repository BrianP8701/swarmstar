from aga_swarm.utils.action_space_utils import delete_action_space_node
from aga_swarm.utils.swarm_utils import get_action_space_metadata
from aga_swarm.swarm.types.metadata import ActionSpaceMetadata
import json

with open('aga_swarm/actions/action_space_metadata.json', 'r') as f:
    action_space_metadata = f.read()
    
# Turn json string into dict
action_space_metadata = json.loads(action_space_metadata)


print(type(action_space_metadata))


delete_action_space_node('aga_swarm/actions/swarm/actions/action_types', action_space_metadata)