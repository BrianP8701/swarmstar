from aga_swarm.core.swarm.swarm import setup_swarm_blueprint, create_swarm_instance
import os
print('here')
goal = '''Go through the data folder in actions. look at all the actions inside, 
which consist of mac platform operations. in addition to those add corresponding 
operations for windows, linux file system,  azure gcp and aws blob storage'''



blueprint_id = setup_swarm_blueprint('my_local_swarm', os.getenv('OPENAI_API_KEY'), '', 'mac', '/Users/brianprzezdziecki/Code/autonomous-general-agent-swarm/z')
swarm_id = create_swarm_instance(blueprint_id, 'my_local_swarm_instance')
print(swarm_id)