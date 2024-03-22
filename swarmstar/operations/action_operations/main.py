"""
The spawn operation will create a new node in the swarm, and begin executing the action assigned to the node.
"""
from typing import List, Union

from swarmstar.models import (
    SwarmOperation,
    ActionOperation,
    SwarmNode,
    ActionMetadata
)
from swarmstar.operations.action_operations.internal_action import execute_action as execute_internal_action

def execute_action(action_operation: ActionOperation) -> Union[SwarmOperation, List[SwarmOperation]]:
    """
    Handles the action and returns the next set of operations
    to perform.
    """
    node_id = action_operation.node_id
    node = SwarmNode.read(node_id)
    action_metadata = ActionMetadata.get(node.type)


    if action_metadata.internal:
        return execute_internal_action(action_operation)
    else:
        raise NotImplementedError("External actions are not yet supported")

