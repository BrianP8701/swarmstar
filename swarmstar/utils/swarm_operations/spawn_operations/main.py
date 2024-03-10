"""
The spawn operation will create a new node in the swarm and return an ActionOperation
"""
from typing import List

from swarmstar.types import (
    SpawnOperation,
    SwarmConfig,
    SwarmNode,
    ActionOperation
)
from swarmstar.utils.swarmstar_space import (
    get_swarm_node, 
    update_swarm_node, 
    save_swarm_node, 
    get_action_metadata,
    add_node_id_to_swarm_state,
    update_swarm_operation
)

def spawn(swarm: SwarmConfig, spawn_operation: SpawnOperation) ->  List[ActionOperation]:
    """
    Swarmstar Spawn Operation handler
    """
    node = _spawn_node(swarm, spawn_operation)
    _update_parent(swarm, spawn_operation, node)
    _update_spawn_operation(swarm, spawn_operation, node.id)

    return ActionOperation(
        node_id=node.id,
        function_to_call="main",
    )


def _spawn_node(swarm: SwarmConfig, spawn_operation: SpawnOperation) -> SwarmNode:
    """
    Spawns a new node in the swarm and saves it to database
    """
    parent_id = spawn_operation.node_id
    node_embryo = spawn_operation.node_embryo
    action_id = node_embryo.action_id
    action_metadata = get_action_metadata(swarm, action_id)
    termination_policy = action_metadata.termination_policy
    
    node = SwarmNode(
        name=action_metadata.name,
        parent_id=parent_id,
        action_id=action_id,
        message=node_embryo.message,
        alive=True,
        termination_policy=termination_policy
    )

    save_swarm_node(swarm, node)
    add_node_id_to_swarm_state(swarm, node.id)
    
    return node

def _update_parent(swarm: SwarmConfig, spawn_operation: SpawnOperation, node: SwarmNode) -> None:
    """
    Update parent node's children_ids and termination_policy if necessary
    """
    parent_id = spawn_operation.node_id
    if parent_id is not None:
        parent_node = get_swarm_node(swarm, parent_id)
        parent_node.children_ids.append(node.id)
        update_swarm_node(swarm, parent_node)

    if spawn_operation.termination_policy_change is not None:
        parent_node = get_swarm_node(swarm, parent_id)
        parent_node.termination_policy = spawn_operation.termination_policy_change
        update_swarm_node(swarm, parent_node)

def _update_spawn_operation(swarm: SwarmConfig, spawn_operation: SpawnOperation, node_id: str) -> None:
    """
    Update child_node_id attr in spawn_operation
    """
    spawn_operation.child_node_id = node_id
    update_swarm_operation(swarm, spawn_operation)
