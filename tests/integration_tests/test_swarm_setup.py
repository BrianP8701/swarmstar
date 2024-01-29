from aga_swarm.swarm.swarm_config import setup_swarm_blueprint, create_swarm_instance
import os

blueprint_id = setup_swarm_blueprint('gratamatta', os.getenv('OPENAI_API_KEY'), '', 'mac', '/Users/brianprzezdziecki/Code/autonomous-general-agent-swarm/z')
swarm_id = create_swarm_instance(blueprint_id, 'instance')
