import pymongo
from pymongo import MongoClient

from swarmstar.types import SwarmConfig, SwarmNode
from swarmstar.utils.swarmstar_space import get_swarm_node, add_node_to_swarm_state, get_action_metadata
from swarmstar.utils.data import get_kv, get_internal_action_metadata


action = get_internal_action_metadata("swarmstar/actions/reasoning")
print(action)