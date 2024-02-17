import os
import pytest

from swarm_star.swarm.setup import setup_swarm_space

@pytest.mark.mac
def test_setup_swarm_space():
    openai_key = os.environ.get('OPENAI_KEY')
    mongodb_uri = os.environ.get('MONGODB_URI')
    mongodb_db_name = 'swarm_1'
    swarm = setup_swarm_space(openai_key, '/Users/brianprzezdziecki/Code/autonomous-general-agent-swarm/my_swarms/test_2_12_24', 'mac', mongodb_uri=mongodb_uri, mongodb_db_name=mongodb_db_name)
    print(swarm)
    
test_setup_swarm_space()