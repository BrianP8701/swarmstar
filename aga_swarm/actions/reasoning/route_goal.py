from typing import List, Optional, Union
from pydantic import BaseModel, Field, Dict

from aga_swarm.swarm.types import Swarm, BlockingOperation, ActionSpace, LifecycleCommand, ActionMetadata, NodeOutput, SwarmCommand

class NextActionPath(BaseModel):
    index: Optional[int] = Field(None, description="Index of the best action path to take")
    failure_message: Optional[str] = Field(None, description="There's no good action path to take. Describe what type of action is needed in detail.")
    
    
def main(swarm: Swarm, node_id: str, message: str) -> BlockingOperation:
    '''
    okay the action router takes the goal. it starts at the root space of the action space
    
    get all the children and their descriptions. pass those along with the goal to instructor have it choose.
    '''
    action_space = ActionSpace(swarm=swarm)
    root: ActionMetadata = action_space['aga_swarm/actions']
    root_children_descriptions = get_children_descriptions(action_space, root)
    messages = build_messages(message, root_children_descriptions)
    return BlockingOperation(
        lifecycle_command=LifecycleCommand.BLOCKING_OPERATION,
        node_id=node_id,
        type="openai_instructor_completion",
        args={
            "messages": messages,
            "model": NextActionPath,
            "swarm": swarm
        },
        context = {
            "parent_action_id": 'aga_swarm/actions',
            "goal": message
        },
        next_function_to_call="route_goal"
    )
    
    
def route_goal(swarm: Swarm, next_action_path: NextActionPath, parent_action_id: str, goal: str) -> Union[BlockingOperation, NodeOutput]:
    '''
    action_id, next_action_index or failure message
    -> 
    '''
    if next_action_path.index is not None:
        action_space = ActionSpace(swarm=swarm)
        parent_action_metadata = action_space[parent_action_id]
        next_action_id = parent_action_metadata.children[next_action_path.index]
        action_metadata = action_space[next_action_id]
        if action_metadata.is_folder:
            children_descriptions = get_children_descriptions(action_space, action_metadata)
            messages = build_messages(goal, children_descriptions)
            return BlockingOperation(
                lifecycle_command=LifecycleCommand.BLOCKING_OPERATION,
                node_id=next_action_id,
                type="openai_instructor_completion",
                args={
                    "messages": messages,
                    "model": NextActionPath,
                    "swarm": swarm
                },
                context = {
                    "parent_action_id": next_action_id,
                    "goal": goal
                },
                next_function_to_call="route_goal"
            )
        else:
            return NodeOutput(
                lifecycle_command=LifecycleCommand.EXECUTE,
                swarm_commands = [
                    SwarmCommand(
                        action_id=next_action_id,
                        message=goal
                    )
                ],
                report = f"Routed goal: {goal} to {next_action_id}"
            )
    else:
        pass
        # Handle failure message. Pass to action creator or user for review
    
    
def build_messages(goal: str, children_descriptions: List[str]) -> List[Dict[str, str]]:
    system_instructions = ('Decide what action path to take based on the goal and the available actions. '
                           'If there is no good action path to take, describe what type of action is needed in detail.')
    
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
    children = []
    for child in action_folder.children:
        child_metadata = action_space[child]
        children.append(child_metadata.description)
    return children

