from pydantic import validate_arguments
from typing import List

from aga_swarm.swarm.types import *
from aga_swarm.actions.swarm.action_types.action import action
from aga_swarm.swarm.swarm_utils import get_action_type, get_action_name, update_state, update_history
from aga_swarm.utils.uuid import generate_uuid

@validate_arguments
def swarm_master(swarm_id, swarm_node: SwarmNode) -> List[SwarmNode]:
    node_output: NodeOutput = execute_node(swarm_node)
    swarm_node.report = node_output.node_report
    lifecycle_command = node_output.lifecycle_command
    
    if lifecycle_command is "success":
        child_nodes = []
        for swarm_command in node_output.swarm_commands:
            child_node = spawn_node(swarm_id, swarm_command, swarm_node.node_id)
            swarm_node.children_ids.append(child_node.node_id)
            child_nodes.append(child_node)
    elif lifecycle_command is 'terminate':
        terminate_node(swarm_node)      
    elif lifecycle_command is 'node_failure':
        pass
    else:
        raise Exception(f"Unknown action_id: {lifecycle_command}")
    return child_nodes

@validate_arguments
def execute_node(swarm_id: SwarmID, node: SwarmNode) -> NodeOutput:
    node_output = action(action_id=node.action_id, 
           action_type=get_action_type(swarm_id, node.action_id), 
           params=node.incoming_swarm_command.action.params,
           swarm_id=swarm_id)
    
    if not isinstance(node_output, NodeOutput):
        raise TypeError("Expected action() to return a NodeOutput instance")
    
    return node_output

@validate_arguments
def spawn_node(swarm_id: SwarmID, swarm_command: SwarmCommand, parent_id: str) -> SwarmNode:
    node = SwarmNode(
        node_id=generate_uuid(get_action_name(swarm_id, swarm_command.action_id)),
        parent_id=parent_id,
        children_ids=[],
        swarm_command=swarm_command,
        alive=True
    )
    update_state(swarm_command.swarm_id, node)
    update_history(swarm_id, LifecycleCommand.SPAWN, node.node_id)
    return node
    
@validate_arguments
def terminate_node(swarm_command: SwarmCommand) -> dict:
    pass

@validate_arguments
def handle_node_failure(swarm_id: SwarmID, node: SwarmNode) -> SwarmNode:
    node.alive = False
    update_state(swarm_id, node)
    update_history(swarm_id, LifecycleCommand.NODE_FAILURE, node.node_id)
    return node