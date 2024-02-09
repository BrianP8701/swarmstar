from pydantic import BaseModel, Field
from typing import List

from aga_swarm.swarm.types import Swarm, SwarmCommand, LifecycleCommand, BlockingOperation, NodeOutput


class DecomposeDirective(BaseModel):
    subdirectives: List[str] = Field(..., description="List of subdirectives to be executed in parallel.")


def main(swarm: Swarm, node_id: str, message: str) -> BlockingOperation:

        
    system_instructions = ('Generate subgoals based on available information, ensuring they are independent '
                           'and can be pursued simultaneously without relying on the completion of other goals. '
                           'Equip each subgoal with necessary details for immediate and independent'
                           'execution. Identify and list subgoals that can operate concurrently, excluding '
                           'sequential or interdependent tasks. This approach facilitates immediate parallel '
                           'execution and efficiency. Subgoals may be complex goals that need to be further '
                           'broken down. Specific subgoals can include anything, from asking the user questions, '
                           'writing code, doing research, browsing the internet etc.')
    messages = [
        {
            "role": "system",
            "content": system_instructions
        },
        {
            "role": "user",
            "content": f'Directive: \n`{message}`'
        }
    ]
    
    return BlockingOperation(
        lifecycle_command=LifecycleCommand.BLOCKING_OPERATION,
        node_id=node_id,
        type="openai_instructor_completion",
        args={
            "messages": messages,
            "model": DecomposeDirective,
            "swarm": swarm
        },
        next_function_to_call="subdirectives_to_swarm_commands"
    )
    

def subdirectives_to_swarm_commands(swarm: Swarm, node_id: str, message: str, model: DecomposeDirective) -> NodeOutput:
    subdirectives = model.subdirectives

    swarm_commands = []
    for subdirective in subdirectives:
        swarm_command = SwarmCommand(
            action_id='aga_swarm/actions/swarm/actions/route_to_action',
            directive= subdirective
        )
        swarm_commands.append(swarm_command)
    
    return NodeOutput(
        lifecycle_command=LifecycleCommand.SPAWN,
        swarm_commands=swarm_commands,
        report=f'Decomposed directive: \n`{message}`\n\nInto subdirectives:\n' + '\n'.join(subdirectives)
    )
