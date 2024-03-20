"""
The action metadata tree allows the swarm to find actions to take.
"""
from swarmstar.models.base_tree import BaseTree

class SwarmTree(BaseTree):
    collection = "swarm_nodes"
