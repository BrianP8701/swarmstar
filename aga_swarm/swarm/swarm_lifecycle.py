from pydantic import validate_call
from typing import List, Union

from aga_swarm.swarm.types import *
from aga_swarm.swarm_utils.misc.uuid import generate_uuid
from aga_swarm.swarm.executor import execute_action

@validate_call
def swarm_master(swarm: Swarm, swarm_node: SwarmNode) -> List[SwarmNode]:
    node_output: NodeIO = _execute_node(swarm, swarm_node)
    swarm_node.report = node_output.report
    lifecycle_command = node_output.lifecycle_command.value
    
    if lifecycle_command == "spawn":
        return _spawn_children(swarm, swarm_node, node_output)
    elif lifecycle_command == 'terminate':
        # TODO handle termination
        return _terminate_node(swarm_node)      
    elif lifecycle_command == 'node_failure':
        # TODO handle node failure
        print(f"Node failure: {swarm_node.report}")
    else:
        raise Exception(f"Unknown action_id: {lifecycle_command}")

'''
Private methods
'''

def _spawn_children(swarm: Swarm, swarm_node: SwarmNode, node_output: NodeIO) -> List[SwarmNode]:
    child_nodes = []
    for swarm_command in node_output.swarm_commands:
        child_node = _spawn_node(swarm, swarm_command, swarm_node.node_id)
        swarm_node.children_ids.append(child_node.node_id)
        child_nodes.append(child_node)
        
    swarm.update_state(swarm_node)
    swarm.update_history(LifecycleCommand.EXECUTE, swarm_node.node_id)
    return child_nodes

def _execute_node(swarm: Swarm, node: SwarmNode) -> NodeIO:
    # TODO Make execute node work properly
    node_output = execute_action(
        action_id=node.swarm_command.action_id, 
        directive=node.swarm_command.directive,
        node_id=node.node_id,
        swarm=swarm)
    
    if not isinstance(node_output, NodeIO):
        raise TypeError("Expected action() to return a NodeIO instance")
    
    return node_output

def _spawn_node(swarm: Swarm, swarm_command: SwarmCommand, parent_id: Union[str, None] = None) -> SwarmNode:
    node = SwarmNode(
        node_id=generate_uuid(swarm.get_action_space_metadata().get_action_name(swarm_command.action_id)),
        parent_id=parent_id,
        children_ids=[],
        swarm_command=swarm_command,
        alive=True
    )
    swarm.update_state(node)
    swarm.update_history(LifecycleCommand.SPAWN, node.node_id)
    return node
    
def _terminate_node(swarm_command: SwarmCommand) -> dict:
    # We need the review reports action here
    pass

def _handle_node_failure(swarm: Swarm, node: SwarmNode) -> SwarmNode:
    pass