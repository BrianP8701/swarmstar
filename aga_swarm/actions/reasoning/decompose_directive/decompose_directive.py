from pydantic import BaseModel, Field
import traceback
from typing import List

from aga_swarm.swarm.types import NodeIO, Swarm, SwarmCommand, LifecycleCommand, NodeIO, BlockingOperation
from aga_swarm.utils.ai.openai_instructor import completion


class DecomposeDirective(BaseModel):
    subdirectives: List[str] = Field(..., description="List of subdirectives to be executed in parallel.")


def main(swarm: Swarm, node_id: str, directive: str) -> NodeIO:

        
    system_instructions = ('Generate subgoals based on available information, ensuring they are independent '
                           'and can be pursued simultaneously. Equip each subgoal with necessary details for '
                           'execution. Identify and list subgoals that can operate concurrently, excluding '
                           'sequential or interdependent tasks. This approach facilitates immediate parallel '
                           'execution and efficiency.')
    messages = [
        {
            "role": "system",
            "content": system_instructions
        },
        {
            "role": "user",
            "content": f'Directive: \n`{directive}`'
        }
    ]
    
    return BlockingOperation(
        node_id=node_id,
        swarm=swarm,
        type="openai_instructor_completion",
        args={
            "messages": messages,
            "model": DecomposeDirective,
            "swarm": swarm
        },
        next_function_to_call="subdirectives_to_swarm_commands"
    )
    

def subdirectives_to_swarm_commands(swarm: Swarm, node_id: str, directive: str, model: DecomposeDirective) -> NodeIO:
    subdirectives = model.subdirectives

    swarm_commands = []
    for subdirective in subdirectives:
        swarm_command = SwarmCommand(
            action_id='aga_swarm/actions/swarm/actions/route_to_action',
            params = {
                'directive': subdirective,
                'swarm': swarm
            }
        )
        swarm_commands.append(swarm_command)
    
    return NodeIO(
        lifecycle_command=LifecycleCommand.SPAWN,
        swarm_commands=swarm_commands,
        report=f'Decomposed directive: \n`{directive}`\n\nInto subdirectives:\n' + '\n'.join(subdirectives)
    )
