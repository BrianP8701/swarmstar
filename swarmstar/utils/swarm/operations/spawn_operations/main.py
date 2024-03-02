"""
The spawn operation will create a new node in the swarm, and begin executing the action assigned to the node.
"""
from importlib import import_module
from typing import List, Union

from swarmstar.swarm.types import (
    SpawnOperation,
    SwarmConfig,
    SwarmNode,
    SwarmOperation,
)
from swarmstar.utils.swarm.swarmstar_space.swarm_state import get_node_from_swarm_state, add_node_to_swarm_state, set_node_in_swarm_state
from swarmstar.utils.swarm.swarmstar_space.action_space import get_action_metadata
from swarmstar.utils.swarm.swarmstar_space.swarm_history import add_event_to_swarm_history

def spawn(
    swarm: SwarmConfig, spawn_operation: SpawnOperation
) -> Union[SwarmOperation, List[SwarmOperation]]:

    parent_id = spawn_operation.node_id
    node_embryo = spawn_operation.node_embryo
    action_id = node_embryo.action_id

    action_metadata = get_action_metadata(swarm, action_id)
    termination_policy = action_metadata.termination_policy
    if spawn_operation.termination_policy_change is not None:
        termination_policy = spawn_operation.termination_policy_change

    node = SwarmNode(
        parent_id=parent_id,
        action_id=action_id,
        message=node_embryo.message,
        alive=True,
        termination_policy=termination_policy,
    )
    
    add_node_to_swarm_state(swarm, node)

    if parent_id is not None:
        parent_node = get_node_from_swarm_state(swarm, parent_id)
        parent_node.children_ids.append(node.id)
        set_node_in_swarm_state(swarm, parent_node)

    add_event_to_swarm_history(swarm, spawn_operation)
    output = execute_node_action(swarm, node, action_metadata)
    return output


def execute_node_action(
    swarm: SwarmConfig, node: SwarmNode, action_metadata
) -> Union[SwarmOperation, List[SwarmOperation]]:
    action_type = action_metadata.type

    action_type_map = {
        "internal_action": "swarmstar.utils.swarm.operations.spawn_operations.internal_action",
    }

    if action_type not in action_type_map:
        raise ValueError(
            f"Action type: `{action_type}` from action id: `{node.action_id}` is not supported yet."
        )

    action_type_module = import_module(action_type_map[action_type])
    action_output = action_type_module.execute_action(swarm, node, action_metadata)
    return action_output
