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
from swarmstar.utils.context import swarm_id_var


def spawn(spawn_operation: SpawnOperation) ->  List[ActionOperation]:
    """
    Swarmstar Spawn Operation handler
    """
    swarm_id = swarm_id_var.get()
    node = _spawn_node(swarm_id, spawn_operation)
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
    parent_id = spawn_operation.parent_node_id
    node_embryo = spawn_operation.node_embryo
    action_id = node_embryo.action_id
    action_metadata = ActionMetadata.get(action_id)
    termination_policy = action_metadata.termination_policy
    
    node = SwarmNode(
        name=action_metadata.name,
        parent_id=parent_id,
        action_id=action_id,
        message=node_embryo.message,
        alive=True,
        termination_policy=termination_policy,
        context=node_embryo.context
    )

    SwarmNode.save(node)
    swarm_id = swarm_id_var.get()
    SwarmState.append(swarm_id, node.id)
    
    return node

def _update_parent(spawn_operation: SpawnOperation, node: SwarmNode) -> None:
    """
    Update parent node's children_ids and termination_policy if necessary
    """
    parent_id = spawn_operation.parent_node_id
    if parent_id is not None:
        parent_node = SwarmNode.get(parent_id)
        parent_node.children_ids.append(node.id)
        SwarmNode.update_swarm_node(parent_node)

def _update_spawn_operation(spawn_operation: SpawnOperation, node_id: str) -> None:
    """
    Update node_id attr in spawn_operation
    """
    spawn_operation.node_id = node_id
    SwarmOperation.update_swarm_operation(spawn_operation)
