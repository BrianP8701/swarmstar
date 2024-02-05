from aga_swarm.swarm.setup_swarm_space import setup_swarm_blueprint, create_swarm_instance
import os

blueprint_id = setup_swarm_blueprint('gratamatta', os.getenv('OPENAI_API_KEY'), '', 'mac', '/Users/brianprzezdziecki/Code/autonomous-general-agent-swarm/z')
swarm = create_swarm_instance(blueprint_id, 'instance')
