from typing import List, Union
import json

from aga_swarm.swarm.types import Swarm, ActionSpace, SwarmCommand, SwarmNode, SwarmState, SwarmHistory, BlockingOperation, NodeOutput, LifecycleCommand
from aga_swarm.utils.misc.uuid import generate_uuid
from aga_swarm.utils.action_utils.execute_action.main import execute_node_action

def spawn_node(swarm: Swarm, swarm_command: SwarmCommand, parent_id: Union[str, None] = None) -> SwarmNode:
    action_space = ActionSpace(swarm=swarm)
    swarm_state = SwarmState(swarm=swarm)
    swarm_history = SwarmHistory(swarm=swarm)
    node = SwarmNode(
        node_id=generate_uuid(action_space[swarm_command.action_id]),
        parent_id=parent_id,
        children_ids=[],
        action_id=swarm_command.action_id,
        message=swarm_command.message,
        report=None,
        alive=True
    )
    swarm_state.update_state(node)
    swarm_history.add_event(LifecycleCommand.SPAWN, node.node_id)
    return node

def execute_node(swarm: Swarm, node: SwarmNode) -> Union[List[SwarmNode], BlockingOperation]:
    node_output: Union[NodeOutput, BlockingOperation] = execute_node_action(swarm, node)
    
    if node_output.lifecycle_command == LifecycleCommand.BLOCKING_OPERATION:
        return BlockingOperation(node_output)
    elif node_output.lifecycle_command == LifecycleCommand.SPAWN:
        return _spawn_children(swarm, node, NodeOutput(node_output))
    elif node_output.lifecycle_command == LifecycleCommand.TERMINATE:
        return _terminate_node(swarm, node, node_output)
    elif node_output.lifecycle_command == LifecycleCommand.NODE_FAILURE:
        return _handle_node_failure(swarm, node, node_output)
    else:
        raise ValueError("Unexpected output type")


'''
Private methods
'''

def _spawn_children(swarm: Swarm, parent: SwarmNode, node_output: NodeOutput) -> List[SwarmNode]:
    parent.report = node_output.report
    children = []
    for swarm_command in node_output.swarm_commands:
        child_node = spawn_node(swarm, swarm_command, parent.node_id)
        parent.children_ids.append(child_node.node_id)
        children.append(child_node)
    
    swarm_state = SwarmState(swarm=swarm)
    swarm_history = SwarmHistory(swarm=swarm)
    swarm_state.update_state(parent)
    swarm_history.add_event(LifecycleCommand.EXECUTE, parent)

    return children

def _terminate_node(swarm: Swarm, node: SwarmNode, node_output: NodeOutput) -> dict:
    '''
        Terminates a node and recursively terminates its parent nodes until a manager or root node is encountered.

        1. Directly terminate the specified node.
        2. Recursively check and potentially terminate parent nodes:
        - Termination stops at the root node.
        - For a manager node:
            - If any child nodes are alive, termination of the manager is halted.
            - If all child nodes are dead and the manager has been reviewed, the manager is terminated.
            - If all child nodes are dead but the manager hasn't been reviewed, initiate a review reports node for all child reports.
    '''
    swarm_state = SwarmState(swarm=swarm)
    node.report = node_output.report
    _node_funeral(swarm, node)    
    
    while node.parent_id is not None:
        node = swarm_state[node.parent_id]
        if node.action_id == 'aga_swarm/actions/reasoning/decompose_directive':
            is_node_reviewed = False
            for child_id in node.children_ids:
                child_node = swarm_state[child_id]
                if child_node.alive:
                    return None
                else:
                    if child_node.action_id == 'aga_swarm/actions/reasoning/review_reports':
                        is_node_reviewed = True
            if not is_node_reviewed:
                reports = _get_reports_of_children(swarm, node)
                return spawn_node(
                    swarm, 
                    SwarmCommand(
                        action_id='aga_swarm/actions/reasoning/review_reports', 
                        message=json.dumps(reports)
                    ), 
                    node.node_id
                )
            else: 
                _node_funeral(swarm, node)
        else:
            _node_funeral(swarm, node)

    return None

def _get_reports_of_children(swarm: Swarm, parent: SwarmNode) -> List[List[str]]:
    reports = []
    swarm_state = SwarmState(swarm=swarm)
    # Visit all branches of this node
    for branch in parent.children_ids:
        node = swarm_state[branch]
        this_branch_reports = []
        this_branch_reports.append(node.report)
        # Iterate until branch ends or we encounter a manager
        while node.children_ids != []:
            node = swarm_state[node.children_ids[0]]
            if node.action_id == 'aga_swarm/actions/reasoning/decompose_directive':
                this_branch_reports.append(node.report)
                break
            else:
                this_branch_reports.append(node.report)
                
        reports.append(this_branch_reports)
    return reports

def _node_funeral(swarm: Swarm, node: SwarmNode) -> SwarmNode:
    # R.I.P my boy    #LongLiveNode #NodeLivesMatterToo  
    node.alive = False
    swarm_state = SwarmState(swarm=swarm)
    swarm_history = SwarmHistory(swarm=swarm)
    swarm_state.update_state(node)
    swarm_history.add_event(LifecycleCommand.TERMINATE, node)

def _handle_node_failure(swarm: Swarm, node: SwarmNode) -> SwarmNode:
    pass