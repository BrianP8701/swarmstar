import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from swarm.utils.space_tree_to_string import create_tree_from_json


print(create_tree_from_json('swarm/actions/tree.json'))