"""
The spawn operation will create a new node in the swarm, and begin executing the action assigned to the node.
"""
from importlib import import_module
from typing import List, Union

from swarmstar.models import (
    SwarmOperation,
    ActionOperation,
    SwarmNode,
    ActionMetadata
)

def execute_action(action_operation: ActionOperation) -> Union[SwarmOperation, List[SwarmOperation]]:
    """
    Handles the action and returns the next set of operations
    to perform.
    """
    node_id = action_operation.node_id
    node = SwarmNode.get_swarm_node(node_id)
    action_metadata = ActionMetadata.get_action_metadata(node.action_id)

    action_type = action_metadata.type

    action_type_map = {
        "internal_action": "swarmstar.utils.swarm_operations.action_operations.internal_action",
    }

    if action_type not in action_type_map:
        raise ValueError(
            f"Action type: `{action_type}` from action id: `{node.action_id}` is not supported yet."
        )

    action_type_module = import_module(action_type_map[action_type])
    return action_type_module.execute_action(action_operation)
