"""
    Parralel review termination is designated decompose directive actions.
    
    A node of this type decomposes its directive into immediate parralelizable actionable subdirectives.
    Thus it will have multiple children, and in addition it's goal might not be accomplished even when
    all it's children have terminated. We thus have a specific termination policy for node' of this type.
    
    1. If any children are alive, do nothing.
    2. If all children are terminated spawn the 'confirm_completion' node.
    3. If all children are terminated including a 'confirm_completion' node, spawn
    a 'consolidate_reports' node
    4. If all children are terminated including a 'consolidate_reports' node, append the
    'consolidate_reports' node's report to this node's reports and terminate.
"""

from typing import Union

from swarmstar.swarm.types import (
    NodeEmbryo,
    SpawnOperation,
    SwarmConfig,
    SwarmState,
    TerminationOperation,
)


def terminate(
    swarm: SwarmConfig, termination_operation: TerminationOperation
) -> Union[TerminationOperation, None]:
    node_id = termination_operation.node_id
    swarm_state = SwarmState(swarm=swarm)
    node = swarm_state[node_id]

    mission_completion = False
    reports_consolidated = False
    node_with_final_report = ""

    for child_id in node.children_ids:
        child = swarm_state[child_id]
        if child.alive:
            return None
        if child.action_id == "swarmstar/actions/reasoning/confirm_completion":
            mission_completion = True
        if child.action_id == "swarmstar/actions/reasoning/consolidate_reports":
            reports_consolidated = True
            node_with_final_report = swarm_state[child_id]

    if mission_completion == False:
        return SpawnOperation(
            operation_type="spawn",
            node_id=node_id,
            node_embryo=NodeEmbryo(
                node_id=node_id,
                action_id="swarmstar/actions/reasoning/confirm_completion",
                message="",
            ),
        )
    else:
        if reports_consolidated == False:
            return SpawnOperation(
                operation_type="spawn",
                node_id=node_id,
                node_embryos=[
                    NodeEmbryo(
                        node_id=node_id,
                        action_id="swarmstar/actions/reasoning/consolidate_reports",
                        message="",
                    )
                ],
            )
        else:
            node.report = node_with_final_report.report
            node.alive = False
            swarm_state.update_state(node)
            return TerminationOperation(
                operation_type="terminate",
                node_id=node_id,
            )
