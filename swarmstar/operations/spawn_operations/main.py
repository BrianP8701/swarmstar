"""
The spawn operation will create a new node in the swarm and return an ActionOperation
"""
from typing import List

from swarmstar.models import (
    SpawnOperation,
    SwarmNode,
    ActionOperation,
    ActionMetadata,
    SwarmOperation
)

def spawn(spawn_operation: SpawnOperation) ->  List[ActionOperation]:
    """
    Swarmstar Spawn Operation handler
    """
    node = _spawn_node(spawn_operation)
    _update_parent(spawn_operation, node)
    _update_spawn_operation(spawn_operation, node.id)

    return ActionOperation(
        node_id=node.id,
        function_to_call="main",
    )

def _spawn_node(spawn_operation: SpawnOperation) -> SwarmNode:
    """
    Spawns a new node in the swarm and saves it to database
    """
    parent_id = spawn_operation.parent_id
    action_id = spawn_operation.action_id
    action_metadata = ActionMetadata.get(action_id)
    termination_policy = action_metadata.termination_policy
    
    node = SwarmNode(
        name=action_metadata.name,
        parent_id=parent_id,
        type=action_id,
        message=spawn_operation.message,
        alive=True,
        termination_policy=termination_policy,
        context=spawn_operation.context
    )

    SwarmNode.insert(node)
    return node

def _update_parent(spawn_operation: SpawnOperation, node: SwarmNode) -> None:
    """
    Update parent node's children_ids and termination_policy if necessary
    """
    parent_id = spawn_operation.parent_id
    if parent_id is not None:
        parent_node = SwarmNode.get(parent_id)
        parent_node.children_ids.append(node.id)
        SwarmNode.replace(parent_node)

def _update_spawn_operation(spawn_operation: SpawnOperation, node_id: str) -> None:
    """
    Update node_id attr in spawn_operation
    """
    spawn_operation.node_id = node_id
    SwarmOperation.replace(spawn_operation)
