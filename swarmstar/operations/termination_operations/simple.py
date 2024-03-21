"""
Simple termination terminates the given node and returns a TerminationOperation for the parent node.
"""
from typing import Union

from swarmstar.models import TerminationOperation, SwarmNode

def terminate(termination_operation: TerminationOperation) -> Union[TerminationOperation, None]:
    node_id = termination_operation.node_id
    node = SwarmNode.get(node_id)
    node.alive = False
    SwarmNode.replace(node)

    try:
        parent_node = SwarmNode.get(node.parent_id)
    except:
        return None

    return TerminationOperation(
        terminator_id=node_id,
        node_id=parent_node.id, 
        context=node.context
    )
