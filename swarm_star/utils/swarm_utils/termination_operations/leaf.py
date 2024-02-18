'''
    Leaf termination is when a leaf node is terminated. This node initialized the termination.
    
    The only difference between leaf and simple termination is that we set the node's report in leaf termination.
'''

from typing import Union

from swarm_star.swarm.types import SwarmConfig, TerminationOperation, SwarmState

def execute_termination_operation(swarm: SwarmConfig, termination_operation: TerminationOperation) -> None:
    node_id = termination_operation.node_id
    swarm_state = SwarmState(swarm=swarm)
    node = swarm_state[node_id]
    node.alive = False
    node.report = termination_operation.report
    swarm_state.update_state(node)
    try:
        parent_node = swarm_state[node.parent_id]
    except:
        raise ValueError(f'Leaf Node {node_id} does not have a parent node.')
    
    return TerminationOperation(
        operation_type='terminate',
        node_id=parent_node.node_id,
        report=''
    )