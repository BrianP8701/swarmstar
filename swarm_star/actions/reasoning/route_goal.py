from typing import List, Optional
from pydantic import BaseModel, Field, Dict

from swarm_star.swarm.types import SwarmConfig, BlockingOperation, ActionSpace, ActionMetadata, SpawnOperation, NodeEmbryo, SwarmOperation

class NextActionPath(BaseModel):
    index: Optional[int] = Field(None, description="Index of the best action path to take")
    failure_message: Optional[str] = Field(None, description="There's no good action path to take. Describe what type of action is needed in detail.")
    
system_instructions = (
    'Decide what action path to take based on the goal and the available actions. '
    'If there is no good action path to take, describe what type of action is needed in detail.'
    )
    
def main(swarm: SwarmConfig, node_id: str, message: str, **kwargs) -> BlockingOperation:
    '''
    The main function begins the process of routing the action space from the root node.
    '''
    action_space = ActionSpace(swarm=swarm)
    root: ActionMetadata = action_space['swarm_star/actions']
    root_children_descriptions = get_children_descriptions(action_space, root)
    messages = build_messages(message, root_children_descriptions)
    return BlockingOperation(
        operation_type='blocking_operation',
        node_id=node_id,
        blocking_type="openai_instructor_completion",
        args={
            "messages": messages,
            "instructor_model": NextActionPath
        },
        context = {
            "swarm": swarm,
            "node_id": node_id,
            "parent_action_id": 'swarm_star/actions',
            "goal": message
        },
        next_function_to_call="route_goal"
    )
    
    
def route_goal(swarm: SwarmConfig, node_id: str, parent_action_id: str, goal: str, completion: NextActionPath) -> SwarmOperation:
    '''
    This function gets called over and over again until we reach a leaf node, aka an action.
    '''
    if completion.index is not None:
        action_space = ActionSpace(swarm=swarm)
        parent_action = action_space[parent_action_id]
        next_action_id = parent_action.children[completion.index]
        current_action = action_space[next_action_id]
        if current_action.is_folder:
            children_descriptions = get_children_descriptions(action_space, current_action)
            messages = build_messages(goal, children_descriptions)
            return BlockingOperation(
                operation_type='blocking_operation',
                node_id=node_id,
                blocking_type="openai_instructor_completion",
                args={
                    "messages": messages,
                    "instructor_model": NextActionPath,
                },
                context = {
                    "parent_action_id": next_action_id,
                    "goal": goal,
                    "swarm": swarm,
                    "node_id": node_id
                },
                next_function_to_call="route_goal"
            )
        else:
            return SpawnOperation(
                operation_type='spawn',
                node_id=node_id,
                node_embryos=[
                    NodeEmbryo(
                        action_id=next_action_id,
                        message=goal
                    )
                ],
                report = f"Routed goal: {goal} to {next_action_id}"
            )
    else:
        failure_message = completion.failure_message
        raise ValueError(f"The router agent failed to find a good action path to take. We need to implement something here to handle this. For example we could pass this to the action creator or talk to the user.\n\nThe agent's failure message: {failure_message}")
        # TODO Handle failure message. Pass to action creator or user for review
    
    
def build_messages(goal: str, children_descriptions: List[str]) -> List[Dict[str, str]]:
    action_path_descriptions = ''
    for i, description in enumerate(children_descriptions):
        action_path_descriptions += f"{i}. {description}\n"
        
    messages = [
        {
            "role": "system",
            "content": system_instructions
        },
        {
            "role": "user",
            "content": f'Goal: \n`{goal}`'
        },
        {
            "role": "system",
            "content": action_path_descriptions
        }
    ]
    return messages
    
def get_children_descriptions(action_space: ActionSpace, action_folder: ActionMetadata) -> List[str]:
    children_descriptions = []
    for child in action_folder.children:
        child_metadata = action_space[child]
        children_descriptions.append(child_metadata.description)
    return children_descriptions
