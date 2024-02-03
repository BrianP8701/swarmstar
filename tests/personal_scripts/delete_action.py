from aga_swarm.swarm.types import *
import json
from pydantic import validate_call

with open('/Users/brianprzezdziecki/Code/autonomous-general-agent-swarm/aga_swarm/actions/action_space_metadata.json', 'r') as f:
    action_space_metadata = f.read()
    
# Turn json string into dict
action_space_metadata = json.loads(action_space_metadata)

# Turn dict into SwarmConfig object
action_space_metadata = ActionSpaceMetadata(**action_space_metadata)



@validate_call
def test(action_space_metadata: ActionSpaceMetadata) -> dict:
    print('success')
