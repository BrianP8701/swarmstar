from pydantic import BaseModel, Field
from typing import List, Optional

from tree_swarm.swarm.types import Swarm, SwarmCommand, BlockingOperation, NodeOutput


class DecomposeDirectiveModel(BaseModel):
    scrap_paper: Optional[str] = Field(..., 'Scrap paper for notes, planning etc. (optional)')
    subdirectives: Optional[List[str]] = Field(..., description="List of subdirectives to be executed in parallel, if you have no questions.")
    questions: Optional[List[str]] = Field(..., description="List of questions to ask the user to get more information.")
    
system_instructions = (
    'You are given a directive. You have 2 options:\n'
    '1. Ask the user questions to get more information or clarification.\n'
    '2. Decompose the directive into actionable subdirectives that will be executed independently and in parralel. '
    'After those are done, youll generate the next set of subdirectives. I stress that the subdirectives '
    'must be independent and parallel.'
    )

def main(swarm: Swarm, node_id: str, message: str) -> BlockingOperation:
    
    messages = [
        {
            "role": "system",
            "content": system_instructions
        },
        {
            "role": "user",
            "content": f'Directive to decompose: \n`{message}`'
        }
    ]
    
    return BlockingOperation(
        lifecycle_command='blocking_operation',
        node_id=node_id,
        type="openai_instructor_completion",
        args={
            "messages": messages,
            "instructor_model": DecomposeDirectiveModel
        },
        context={
            "directive": message
        },
        next_function_to_call="analyze_output"
    )
    
def analyze_output(directive: str, completion: DecomposeDirectiveModel) -> NodeOutput:
    if len(completion.questions) > 0:
        message = f'An agent was tasked with decomposing the directive: \n`{directive}`\n\nBefore decomposing, the agent has questions:\n'
        message += '\n'.join(completion.questions)
        
        return NodeOutput(
            lifecycle_command='spawn',
            swarm_commands=[
                SwarmCommand(
                    action_id='tree_swarm/actions/communication/ask_user_questions',
                    message=message
                )
            ],
            report=f'Asked user questions about directive: \n`{directive}`'
        )
    else:
        return subdirectives_to_swarm_commands(directive, completion)

def subdirectives_to_swarm_commands(directive: str, completion: DecomposeDirectiveModel) -> NodeOutput:
    subdirectives = completion.subdirectives

    swarm_commands = []
    for subdirective in subdirectives:
        swarm_command = SwarmCommand(
            action_id='tree_swarm/actions/swarm/actions/route_to_action',
            message=subdirective
        )
        swarm_commands.append(swarm_command)
    
    return NodeOutput(
        lifecycle_command='spawn',
        swarm_commands=swarm_commands,
        report=f'Decomposed directive: \n`{directive}`\n\nInto subdirectives:\n' + '\n'.join(subdirectives)
    )
