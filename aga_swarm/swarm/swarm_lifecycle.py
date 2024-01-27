from pydantic import validate_arguments, List

from aga_swarm.swarm.types import SwarmID, SwarmCommand, NodeOutput, NodeReport
from aga_swarm.actions.swarm.action_types.action import action
from aga_swarm.swarm.swarm_utils import get_swarm_state, get_action_type
from aga_swarm.swarm.swarm_node import SwarmNode
from aga_swarm.utils.uuid import generate_uuid

@validate_arguments
def swarm_master(swarm_node: SwarmNode) -> List[SwarmCommand]:
    node_output = execute_node(swarm_node)
    swarm_node.report = node_output.node_report
    if node_output.node_report.success == True:
        child_nodes = []
        for child_swarm_command in node_output.swarm_commands:
            if child_swarm_command.lifecycle_command is 'spawn':
                child_node = spawn_node(child_swarm_command)
                swarm_node.children_ids.append(child_node.node_id)
                child_node.parent_id = swarm_node.node_id
                child_nodes.append(child_node)
            elif child_swarm_command.lifecycle_command is 'terminate':
                pass
            else:
                raise Exception(f"Unknown action_id: {child_swarm_command.lifecycle_command}")
        return child_nodes
    else:
        # TODO TODO TODO Handle node failure by spawning a node to handle the failure autonomously TODO TODO TODO
        pass

@validate_arguments
def execute_node(swarm_id: SwarmID, node: SwarmNode) -> dict:
    return action(action_id=node.action_id, 
           action_type=get_action_type(swarm_id, node.action_id), 
           params=node.incoming_swarm_command.action.params,
           swarm_id=swarm_id)

@validate_arguments
def spawn_node(swarm_command: SwarmCommand) -> dict:
    return SwarmNode(
        node_id=generate_uuid(),
        action_id=swarm_command.action.action_id,
        parent_id=None,
        children_ids=[],
        incoming_swarm_command=swarm_command,
        report={},
        alive=True
    )

@validate_arguments
def terminate_node(swarm_command: SwarmCommand) -> dict:
    pass

@validate_arguments
def action_executor(action: dict, swarm_id: SwarmID) -> dict:
    return execute(action['type'], swarm_id, action['params'])

