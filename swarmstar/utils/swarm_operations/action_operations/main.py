"""
The spawn operation will create a new node in the swarm, and begin executing the action assigned to the node.
"""
from importlib import import_module
from typing import List, Union

from swarmstar.types import (
    SwarmConfig,
    SwarmOperation,
    ActionOperation
)
from swarmstar.utils.swarmstar_space import (
    get_swarm_node, 
    add_swarm_operation_id_to_swarm_history, 
    get_action_metadata,
    save_swarm_operation,
)

def execute_action(swarm_config: SwarmConfig, action_operation: ActionOperation) -> Union[SwarmOperation, List[SwarmOperation]]:
    """
    Handles the action and returns the next set of operations
    to perform.
    """
    node_id = action_operation.node_id
    node = get_swarm_node(swarm_config, node_id)
    action_metadata = get_action_metadata(swarm_config, node.action_id)

    action_type = action_metadata.type

    action_type_map = {
        "internal_action": "swarmstar.utils.swarm_operations.action_operations.internal_action",
    }

    if action_type not in action_type_map:
        raise ValueError(
            f"Action type: `{action_type}` from action id: `{node.action_id}` is not supported yet."
        )
    
    save_swarm_operation(swarm_config, action_operation)
    add_swarm_operation_id_to_swarm_history(swarm_config, action_operation.id)

    action_type_module = import_module(action_type_map[action_type])
    return action_type_module.execute_action(swarm_config, action_operation)
