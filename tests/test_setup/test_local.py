import os
import pytest

from aga_swarm.swarm.swarm_setup import setup_swarm_space

@pytest.mark.local
def test_setup_swarm_space():
    # GEt openai key from env
    openai_key = os.environ.get('OPENAI_API_KEY')
    setup_swarm_space(openai_key, 'blank for now', '/Users/brianprzezdziecki/Code/autonomous-general-agent-swarm/y', 'mac')
