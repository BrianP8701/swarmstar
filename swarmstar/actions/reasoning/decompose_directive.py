'''
Decompose a directive into actionable subdirectives.

The agent will ask questions if it needs more information before decomposing the directive.
'''

from pydantic import BaseModel, Field
from typing import List, Optional

from swarmstar.swarm.types import NodeEmbryo, BlockingOperation, SpawnOperation, SwarmConfig


class DecomposeDirectiveModel(BaseModel):
    scrap_paper: Optional[str] = Field(None, description='Scrap paper for notes, planning etc. Use this space to think step by step. (optional)')
    questions: Optional[List[str]] = Field(..., description="Questions you need answered before decomposition.")
    subdirectives: Optional[List[str]] = Field(..., description="List of subdirectives to be executed in parallel, if you have no questions.")

system_instructions = (
    'You are given a directive. You have 2 options:\n'
    '1. Ask questions to get more information or clarification of requirements and intentions.\n'
    '2. Decompose the directive into actionable subdirectives that will be executed independently and in parralel. '
    'After those are done, youll generate the next set of subdirectives. I stress that the subdirectives '
    'must be independent and parallel.\n\nChoose one of the options and proceed. Do not ask questions and decompose the directive at the same time.'
    )

def main(swarm: SwarmConfig, node_id: str, message: str, **kwargs) -> BlockingOperation:
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
        node_id=node_id,
        blocking_type="openai_instructor_completion",
        args={
            "messages": messages,
            "instructor_model_name": "DecomposeDirectiveModel"
        },
        context={
            "directive": message,
            "parent_id": node_id
        },
        next_function_to_call="analyze_output"
    )
    
def analyze_output(directive: str, parent_id: str, completion: DecomposeDirectiveModel) -> SpawnOperation:
    if len(completion.questions) > 0:
        message = f'An agent was tasked with decomposing the directive: \n`{directive}`\n\nBefore decomposing, the agent decided it needs the following questions answered first:\n'
        message += '\n'.join(completion.questions)
        
        spawn_operation = SpawnOperation(
            node_id=parent_id,
            node_embryo=NodeEmbryo(
                action_id='swarmstar/actions/communication/ask_user_questions',
                message=message
            ),
            report=(
                f'The agent tasked with decomposing directives decided to ask the user questions '
                'about directive: \n`{directive}`\n\nQuestions:\n' + '\n'.join(completion.questions),
            )
        )
        return spawn_operation
    else:
        return subdirectives_to_swarm_commands(directive, parent_id, completion)

def subdirectives_to_swarm_commands(directive: str, parent_id: str, completion: DecomposeDirectiveModel) -> List[SpawnOperation]:
    subdirectives = completion.subdirectives
    report = f'The agent tasked with decomposing the directive: \n`{directive}`\n\nDecomposed the directive into the following subdirectives:\n'
    spawn_operations = []
    for subdirective in subdirectives:
        node_embryo = NodeEmbryo(
            action_id='swarmstar/actions/swarm/actions/route_action',
            message=subdirective
        )        
        spawn_operations.append(SpawnOperation(
            node_id=parent_id,
            node_embryos=node_embryo
        ))
        
    return spawn_operations
