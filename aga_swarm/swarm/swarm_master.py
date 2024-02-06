from pydantic import validate_call
from typing import List, Union

from aga_swarm.swarm.types import *
from aga_swarm.utils.misc.uuid import generate_uuid

def spawn_node(swarm: Swarm, swarm_command: SwarmCommand, parent_id: Union[str, None] = None) -> SwarmNode:
    action_space = ActionSpace(swarm=swarm)
    swarm_state = SwarmState(swarm=swarm)
    swarm_history = SwarmHistory(swarm=swarm)
    node = SwarmNode(
        node_id=generate_uuid(action_space[swarm_command.action_id]),
        parent_id=parent_id,
        children_ids=[],
        action_id=swarm_command.action_id,
        directive=swarm_command.directive,
        report=None,
        alive=True
    )
    swarm_state.update_node(node.node_id, node)
    swarm_history.update_history(LifecycleCommand.SPAWN, node.node_id)
    return node

def execute_node(swarm: Swarm, swarm_node: SwarmNode):
    node_output = _execute_node_action(swarm, swarm_node)
    
    if node_output.lifecycle_command == LifecycleCommand.BLOCKING_OPERATION:
        return node_output
    elif node_output.lifecycle_command == LifecycleCommand.SPAWN:
        return _spawn_children(swarm, swarm_node, node_output)
    elif node_output.lifecycle_command == LifecycleCommand.TERMINATE:
        return _terminate_node(swarm, swarm_node, node_output)
    elif node_output.lifecycle_command == LifecycleCommand.NODE_FAILURE:
        return _handle_node_failure(swarm, swarm_node, node_output)
    else:
        raise ValueError("Unexpected output type")

def execute_blocking_operation(swarm: Swarm, blocking_operation: BlockingOperation):
    # TODO Make execute_blocking_operation work properly
    pass

'''
Private methods
'''

def _spawn_children(swarm: Swarm, swarm_node: SwarmNode, node_output: NodeOutput) -> List[SwarmNode]:
    child_nodes = []
    for swarm_command in node_output.swarm_commands:
        child_node = spawn_node(swarm, swarm_command, swarm_node.node_id)
        swarm_node.children_ids.append(child_node.node_id)
        child_nodes.append(child_node)
        
    swarm.update_state(swarm_node)
    swarm.update_history(LifecycleCommand.EXECUTE, swarm_node.node_id)
    return child_nodes

def _execute_node_action(swarm: Swarm, node: SwarmNode) -> NodeIO:
    # TODO Make execute node work properly
    node_output = execute_action(
        action_id=node.swarm_command.action_id, 
        directive=node.swarm_command.directive,
        node_id=node.node_id,
        swarm=swarm)
    
    if not isinstance(node_output, NodeIO):
        raise TypeError("Expected action() to return a NodeIO instance")
    
    return node_output


def _terminate_node(swarm_command: SwarmCommand) -> dict:
    # We need the review reports action here
    pass

def _handle_node_failure(swarm: Swarm, node: SwarmNode) -> SwarmNode:
    pass