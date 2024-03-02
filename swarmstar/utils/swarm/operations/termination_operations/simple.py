"""
    Simple termination simply terminates the given node and returns a TerminationOperation for the parent node.
"""
from typing import Union

from swarmstar.swarm.types import SwarmConfig, TerminationOperation
from swarmstar.utils.swarm.swarmstar_space.swarm_state import get_node_from_swarm_state, set_node_in_swarm_state

def terminate(
    swarm: SwarmConfig, termination_operation: TerminationOperation
) -> Union[TerminationOperation, None]:
    node_id = termination_operation.node_id
    node = get_node_from_swarm_state(swarm, node_id)
    node.alive = False
    set_node_in_swarm_state(swarm, node)

    try:
        parent_node = get_node_from_swarm_state(swarm, node.parent_id)
    except:
        return None

    return TerminationOperation(
        node_id=parent_node._id, 
    )
