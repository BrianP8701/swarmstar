from typing import List, Union
import json

from swarm_star.swarm.types import SwarmConfig, ActionSpace, SwarmOperation, SwarmNode, SwarmState, SwarmHistory, BlockingOperation, SpawnOperation, NodeEmbryo, ExecuteOperation, TerminateOperation
from swarm_star.utils.misc.uuid import generate_uuid
from swarm_star.utils.swarm_utils.execute_node.main import execute_node_action
from swarm_star.utils.swarm_utils.execute_blocking_operation.main import execute_blocking_operation as _execute_blocking_operation

def spawn_swarm(goal: str) -> SpawnOperation:
    return SpawnOperation(
        operation_type='spawn',
        node_embedding=[
            NodeEmbryo(
                action_id='swarm_star/actions/reasoning/decompose_directive',
                message=goal
            )
        ]
    )

def swarm_master(swarm: SwarmConfig, swarm_operation: SwarmOperation) -> List[SwarmOperation]:
    if swarm_operation.operation_type == 'spawn':
        nodes = _execute_spawn_operation(swarm, swarm_operation)
        execute_operations = []
        for node in nodes:
            execute_operations.append(ExecuteOperation(
                operation_type='execute',
                node=node
            ))
        return execute_operations
    elif swarm_operation.operation_type == 'blocking_operation':
        return _execute_blocking_operation(swarm, swarm_operation)
    elif swarm_operation.operation_type == 'terminate':
        return _execute_terminate_operation(swarm, swarm_operation)
    elif swarm_operation.operation_type == 'node_failure':
        return _handle_node_failure(swarm, swarm_operation)
    else:
        raise ValueError("Unexpected output type")



    
def execute_swarm_operation(swarm: SwarmConfig, swarm_operation) -> SwarmOperation:
    if swarm_operation.operation_type == 'blocking_operation':
        return execute_blocking_operation(swarm, swarm_operation)
    elif swarm_operation.operation_type == 'spawn':
        return spawn_node(swarm, swarm_operation)
    elif swarm_operation.operation_type == 'terminate':
        return _terminate_node(swarm, swarm_operation)
    elif swarm_operation.operation_type == 'node_failure':
        return _handle_node_failure(swarm, swarm_operation)
    else:
        raise ValueError("Unexpected output type")

'''
Private methods
'''

def _execute_spawn_operation(swarm: SwarmConfig, spawn_operation: SpawnOperation) -> List[SwarmNode]:
    nodes = []
    for node_embryo in spawn_operation.node_embryos:
        node = _spawn_node(swarm, node_embryo, spawn_operation.node_id)
        nodes.append(node)
    return nodes


def _execute_terminate_operation(swarm: SwarmConfig, terminate_operation: TerminateOperation) -> dict:
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
    swarm_history = SwarmHistory(swarm=swarm)

    node.report = terminate_operation.report
    _node_funeral(swarm, node)    
    swarm_history.add_event(terminate_operation)
    
    while node.parent_id is not None:
        node = swarm_state[node.parent_id]
        if node.termination_policy == '':
            if len(node.children_ids) == 1:
                if swarm_state[node.children_ids[0]].action_id == 'swarm_star/actions/reasoning/review_reports':
                    _node_funeral(swarm, node)
                _node_funeral(swarm, node)
            else:
                is_node_reviewed = False
                for child_id in node.children_ids:
                    child_node = swarm_state[child_id]
                    if child_node.alive:
                        return None
                    else:
                        if child_node.action_id == 'swarm_star/actions/reasoning/review_reports':
                            is_node_reviewed = True
                if not is_node_reviewed:
                    reports = _get_reports_of_children(swarm, node)
                    return spawn_node(
                        swarm, 
                        SwarmCommand(
                            action_id='swarm_star/actions/reasoning/review_reports', 
                            message=json.dumps(reports)
                        ), 
                        node.node_id
                    )
                else: 
                    _node_funeral(swarm, node)
        else:
            _node_funeral(swarm, node)

    return None


def _spawn_node(swarm: SwarmConfig, node_embryo: NodeEmbryo, parent_id: str) -> SwarmNode:
    action_space = ActionSpace(swarm=swarm)
    swarm_state = SwarmState(swarm=swarm)
    swarm_history = SwarmHistory(swarm=swarm)
    node_embryo = NodeEmbryo.model_validate(node_embryo)
    node = SwarmNode(
        node_id=generate_uuid(action_space[node_embryo.action_id].name),
        parent_id=parent_id,
        action_id=node_embryo.action_id,
        message=node_embryo.message,
        alive=True
    )
    swarm_state.update_state(node)
    swarm_history.add_event('spawn', node)
    return node

def _spawn_children(swarm: SwarmConfig, parent: SwarmNode, node_output: NodeOutput) -> List[SwarmNode]:
    parent.report = node_output.report
    children = []
    for swarm_command in node_output.swarm_commands:
        child_node = spawn_node(swarm, swarm_command, parent.node_id)
        parent.children_ids.append(child_node.node_id)
        children.append(child_node)
    
    swarm_state = SwarmState(swarm=swarm)
    swarm_history = SwarmHistory(swarm=swarm)
    swarm_state.update_state(parent)
    swarm_history.add_event('execute', parent)

    return children


def _get_reports_of_children(swarm: SwarmConfig, parent: SwarmNode) -> List[List[str]]:
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
            if node.action_id == 'swarm_star/actions/reasoning/decompose_directive':
                this_branch_reports.append(node.report)
                break
            else:
                this_branch_reports.append(node.report)
                
        reports.append(this_branch_reports)
    return reports

def _node_funeral(swarm: SwarmConfig, node: SwarmNode) -> SwarmNode:
    node.alive = False
    swarm_state = SwarmState(swarm=swarm)
    swarm_state.update_state(node)

def _handle_node_failure(swarm: SwarmConfig, node: SwarmNode) -> SwarmNode:
    raise ValueError("Node failed to execute. Didnt write logic to handle node failure yet so this error isnt a bad thing") # TODO: Implement this
    pass