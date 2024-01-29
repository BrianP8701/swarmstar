from pydantic import validate_call
from typing import List, Union

from aga_swarm.swarm.types import *
from aga_swarm.actions.swarm.actions.action_types.action import action
from aga_swarm.utils.swarm_utils import get_action_name, update_state, update_history
from aga_swarm.utils.uuid import generate_uuid

@validate_call
def swarm_master(swarm_id, swarm_node: SwarmNode) -> List[SwarmNode]:
    node_output: NodeOutput = execute_node(swarm_id, swarm_node)
    swarm_node.report = node_output.report
    lifecycle_command = node_output.lifecycle_command.value
    
    if lifecycle_command == "spawn":
        child_nodes = []
        for swarm_command in node_output.swarm_commands:
            child_node = spawn_node(swarm_id, swarm_command, swarm_node.node_id)
            swarm_node.children_ids.append(child_node.node_id)
            child_nodes.append(child_node)
        return child_nodes
    elif lifecycle_command == 'terminate':
        terminate_node(swarm_node)      
    elif lifecycle_command == 'node_failure':
        print(f"Node failure: {swarm_node.report}")
    else:
        raise Exception(f"Unknown action_id: {lifecycle_command}")


@validate_call
def execute_node(swarm_id: SwarmID, node: SwarmNode) -> NodeOutput:
    node_output = action(action_id=node.swarm_command.action_id, 
        params=node.swarm_command.params,
        swarm_id=swarm_id)
    
    if not isinstance(node_output, NodeOutput):
        raise TypeError("Expected action() to return a NodeOutput instance")
    
    return node_output

@validate_call
def spawn_node(swarm_id: SwarmID, swarm_command: SwarmCommand, parent_id: Union[str, None] = None) -> SwarmNode:
    node = SwarmNode(
        node_id=generate_uuid(get_action_name(swarm_id, swarm_command.action_id)),
        parent_id=parent_id,
        children_ids=[],
        swarm_command=swarm_command,
        alive=True
    )
    update_state(swarm_id, node)
    update_history(swarm_id, LifecycleCommand.SPAWN, node.node_id)
    return node
    
@validate_call
def terminate_node(swarm_command: SwarmCommand) -> dict:
    pass

@validate_call
def handle_node_failure(swarm_id: SwarmID, node: SwarmNode) -> SwarmNode:
    node.alive = False
    update_state(swarm_id, node)
    update_history(swarm_id, LifecycleCommand.NODE_FAILURE, node.node_id)
    return node