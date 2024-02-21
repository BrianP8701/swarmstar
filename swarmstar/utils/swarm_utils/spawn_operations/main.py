'''
The spawn operation will create a new node in the swarm, and begin executing the action assigned to the node.
'''
from importlib import import_module
from typing import List, Union

from swarmstar.swarm.types import SwarmConfig, SwarmState, SwarmOperation, SpawnOperation, ActionSpace, SwarmNode, SwarmHistory
from swarmstar.utils.misc.uuid import generate_uuid
from swarmstar.swarm.decorators import swarmstar_decorator

@swarmstar_decorator
def execute_spawn_operation(swarm: SwarmConfig, spawn_operation: SpawnOperation) ->  Union[SwarmOperation, List[SwarmOperation]]:
    
    swarm_state = SwarmState(swarm=swarm)
    action_space = ActionSpace(swarm=swarm)
    
    parent_id = spawn_operation.node_id
    action_id = spawn_operation.node_embryo.action_id
    
    action_metadata = action_space[action_id]
    termination_policy = action_metadata.termination_policy
    
    node = SwarmNode(
        node_id=generate_uuid(action_space[action_id].name),
        parent_id=parent_id,
        action_id=action_id,
        message=spawn_operation.node_embryo.message,
        alive=True,
        termination_policy=termination_policy
    )
    swarm_state.update_state(node)
    
    if parent_id is not None:
        parent_node = swarm_state[parent_id]
        parent_node.children_ids.append(node.node_id)
        swarm_state.update_state(parent_node)


    output = execute_node_action(swarm, node, action_metadata)
    
    swarm_history = SwarmHistory(swarm=swarm)
    swarm_history.add_operation(spawn_operation)
    return output

def execute_node_action(swarm: SwarmConfig, node: SwarmNode, action_metadata) ->  Union[SwarmOperation, List[SwarmOperation]]:
    action_type = action_metadata.type

    action_type_map = {
        'internal_action': 'swarmstar.utils.swarm_utils.spawn_operations.internal_action',
    }
    
    if action_type not in action_type_map:
        raise ValueError(f"Action type: `{action_type}` from action id: `{node.action_id}` is not supported yet.")
    
    action_type_module = import_module(action_type_map[action_type])
    action_output = action_type_module.execute_action(swarm, node, action_metadata)
    
    return action_output