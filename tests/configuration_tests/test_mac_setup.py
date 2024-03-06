import os

import pytest

from tests.utils.create_local_swarm_space import find_next_available_swarm_folder


@pytest.mark.mac
def test_setup_swarm_space():
    root_path = find_next_available_swarm_folder()
    openai_key = os.environ.get("OPENAI_KEY")
    mongodb_uri = os.environ.get("MONGODB_URI")
    mongodb_db_name = "swarmstar_tests"
    # mongodb_db_name = "0"
