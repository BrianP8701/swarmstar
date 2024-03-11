"""
    review_directive_completion is a termination policy for nodes of type 'decompose_directive'.
    
    A node of this type decomposes its directive into immediate parallelizable actionable subdirectives.
    Thus it will have multiple children, and in addition it's goal might not be accomplished even when
    all it's children have terminated. We thus have a specific termination policy for nodes of this type.
    
    1. If any children are alive, do nothing.
    2. If all children are terminated spawn the 'review_directive_completion' node.
    3. If all children are terminated including a 'review_directive_completion' node, 
        terminate the node.
"""

from typing import Union

from swarmstar.utils.swarmstar_space import get_swarm_node, update_swarm_node
from swarmstar.types import (
    NodeEmbryo,
    SpawnOperation,
    SwarmConfig,
    TerminationOperation,
)


def terminate(
    swarm: SwarmConfig, termination_operation: TerminationOperation
) -> Union[TerminationOperation, None]:
    terminator_node_id = termination_operation.terminator_node_id
    target_node_id = termination_operation.target_node_id
    
    target_node = get_swarm_node(swarm, target_node_id)

    if target_node.action_id == "swarmstar/actions/reasoning/review_directive_completion":
        
    
    mission_completion = False
    reports_consolidated = False
    node_with_final_report = ""

    for child_id in node.children_ids:
        child = get_swarm_node(swarm, child_id)
        if child.alive:
            return None
        if child.action_id == "swarmstar/actions/reasoning/confirm_completion":
            mission_completion = True
        if child.action_id == "swarmstar/actions/reasoning/consolidate_reports":
            reports_consolidated = True
            node_with_final_report = get_swarm_node(swarm, child_id)

    if mission_completion == False:
        return SpawnOperation(
            node_id=node_id,
            node_embryo=NodeEmbryo(
                action_id="swarmstar/actions/reasoning/confirm_completion",
                message="",
            ),
        )
    else:
        if reports_consolidated == False:
            return SpawnOperation(
                node_id=node_id,
                node_embryos=[
                    NodeEmbryo(
                        action_id="swarmstar/actions/reasoning/consolidate_reports",
                        message="",
                    )
                ],
            )
        else:
            node.report = node_with_final_report.report
            node.alive = False
            update_swarm_node(swarm, node)
            return TerminationOperation(
                node_id=node_id,
            )
