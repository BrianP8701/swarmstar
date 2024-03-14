from importlib import import_module
from typing import List, Union

from swarmstar.models import SwarmConfig, SwarmOperation, ActionOperation, SwarmNode, ActionMetadata

def execute_action(action_operation: ActionOperation) -> Union[SwarmOperation, List[SwarmOperation]]:
    """
    This handles actions that are internal to swarmstar.
    """
    node_id = action_operation.node_id
    node = SwarmNode.get_swarm_node(node_id)
    action_metadata = ActionMetadata.get_action_metadata(node.action_id)

    internal_action_path = action_metadata.internal_action_path
    action_class = getattr(import_module(internal_action_path), "Action")
    action_instance = action_class(node=node)

    function_to_call = action_operation.function_to_call
    args = action_operation.args

    return getattr(action_instance, function_to_call)(**args)
