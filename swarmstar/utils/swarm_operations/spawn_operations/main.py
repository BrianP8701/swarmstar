"""
The spawn operation will create a new node in the swarm, and begin executing the action assigned to the node.
"""
from importlib import import_module
from typing import List, Union

from swarmstar.types import (
    SpawnOperation,
    SwarmConfig,
    SwarmNode,
    SwarmOperation,
)
from swarmstar.utils.swarmstar_space import (
    get_swarm_node, 
    update_swarm_node, 
    save_swarm_node, 
    add_swarm_operation_to_swarm_history, 
    get_action_metadata,
    save_swarm_operation
)

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
    
    save_swarm_node(swarm, node)

    if parent_id is not None:
        parent_node = get_swarm_node(swarm, parent_id)
        parent_node.children_ids.append(node.id)
        update_swarm_node(swarm, parent_node)

    save_swarm_operation(swarm, spawn_operation)
    add_swarm_operation_to_swarm_history(swarm, spawn_operation.id)
    output = execute_node_action(swarm, node, action_metadata)
    return output


def execute_node_action(
    swarm: SwarmConfig, node: SwarmNode, action_metadata
) -> Union[SwarmOperation, List[SwarmOperation]]:
    action_type = action_metadata.type

    action_type_map = {
        "internal_action": "swarmstar.utils.swarm_operations.spawn_operations.internal_action",
    }

    if action_type not in action_type_map:
        raise ValueError(
            f"Action type: `{action_type}` from action id: `{node.action_id}` is not supported yet."
        )

    action_type_module = import_module(action_type_map[action_type])
    action_output = action_type_module.execute_action(swarm, node, action_metadata)
    return action_output
