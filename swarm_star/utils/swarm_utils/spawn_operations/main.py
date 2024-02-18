from typing import Union, List
from importlib import import_module

from swarm_star.swarm.types import SwarmConfig, SwarmState, SwarmOperation, SpawnOperation, ActionSpace, SwarmHistory, SwarmNode
from swarm_star.utils.misc.uuid import generate_uuid

def execute_spawn_operation(swarm: SwarmConfig, spawn_operation: SpawnOperation) -> SwarmOperation:
    action_type_map = {
        'internal_action': 'swarm_star.utils.swarm_utils.action_operations.internal_action',
    }
    swarm_state = SwarmState(swarm=swarm)
    swarm_history = SwarmHistory(swarm=swarm)

    parent_id = spawn_operation.parent_id
    parent_node = swarm_state[parent_id]
    parent_node.report = spawn_operation.report
    swarm_state.update_state(parent_node)
    
    node_embryo = spawn_operation.node_embryo
    action_id = node_embryo.action_id
    node = SwarmNode(
        node_id=generate_uuid(action_space[action_id].name),
        parent_id=parent_id,
        action_id=action_id,
        message=node_embryo.message,
        alive=True
    )
    swarm_state.update_state(node)
    swarm_history.add_event(spawn_operation)
    
    action_space = ActionSpace(swarm=swarm)
    action_metadata = action_space[action_id]
    action_type = action_metadata.type
    
    if action_type not in action_type_map:
        raise ValueError(f"Action type: `{action_type}` from action id: `{action_id}` is not supported yet.")
    
    action_type_module = import_module(action_type_map[action_type])
    action_output = action_type_module.execute_action(swarm, node, action_metadata)
    
    return action_output