"""
The spawn operation will create a new node in the swarm and return an ActionOperation
"""
from typing import List

from swarmstar.models import (
    SpawnOperation,
    SwarmNode,
    ActionOperation,
    ActionMetadata,
    SwarmState,
    SwarmOperation
)

def spawn(swarm_id: str, spawn_operation: SpawnOperation) ->  List[ActionOperation]:
    """
    Swarmstar Spawn Operation handler
    """
    node = _spawn_node(swarm_id, spawn_operation)
    _update_parent(spawn_operation, node)
    _update_spawn_operation(spawn_operation, node.id)

    return ActionOperation(
        node_id=node.id,
        function_to_call="main",
    )

def _spawn_node(swarm_id: str, spawn_operation: SpawnOperation) -> SwarmNode:
    """
    Spawns a new node in the swarm and saves it to database
    """
    parent_id = spawn_operation.parent_node_id
    node_embryo = spawn_operation.node_embryo
    action_id = node_embryo.action_id
    action_metadata = ActionMetadata.get_action_metadata(action_id)
    termination_policy = action_metadata.termination_policy
    
    node = SwarmNode(
        name=action_metadata.name,
        parent_id=parent_id,
        action_id=action_id,
        message=node_embryo.message,
        alive=True,
        termination_policy=termination_policy,
        context=spawn_operation.context
    )

    SwarmNode.insert_swarm_node(node)
    SwarmState.add_node_id_to_swarm_state(swarm_id, node.id)
    
    return node

def _update_parent(spawn_operation: SpawnOperation, node: SwarmNode) -> None:
    """
    Update parent node's children_ids and termination_policy if necessary
    """
    parent_id = spawn_operation.parent_node_id
    if parent_id is not None:
        parent_node = SwarmNode.get_swarm_node(parent_id)
        parent_node.children_ids.append(node.id)
        SwarmNode.update_swarm_node(parent_node)

def _update_spawn_operation(spawn_operation: SpawnOperation, node_id: str) -> None:
    """
    Update node_id attr in spawn_operation
    """
    spawn_operation.node_id = node_id
    SwarmOperation.update_swarm_operation(spawn_operation)
