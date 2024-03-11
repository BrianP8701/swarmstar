"""
Simple termination terminates the given node and returns a TerminationOperation for the parent node.
"""
from typing import Union

from swarmstar.types import SwarmConfig, TerminationOperation
from swarmstar.utils.swarmstar_space import get_swarm_node, update_swarm_node

def terminate(
    swarm: SwarmConfig, termination_operation: TerminationOperation
) -> Union[TerminationOperation, None]:
    node_id = termination_operation.node_id
    node = get_swarm_node(swarm, node_id)
    node.alive = False
    update_swarm_node(swarm, node)

    try:
        parent_node = get_swarm_node(swarm, node.parent_id)
    except:
        return None

    return TerminationOperation(
        terminator_node_id=node_id,
        target_node_id=parent_node.id, 
        context=termination_operation.context
    )
