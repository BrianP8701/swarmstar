from aga_swarm.core.swarm.swarm import build_swarm_blueprint
import os
print('here')
goal = '''Go through the data folder in actions. look at all the actions inside, 
which consist of mac platform operations. in addition to those add corresponding 
operations for windows, linux file system,  azure gcp and aws blob storage'''



swarm_blueprint = build_swarm_blueprint('my_local_swarm', os.getenv('OPENAI_API_KEY'), '', 'mac', '/Users/brianprzezdziecki/Code/autonomous-general-agent-swarm/z')
