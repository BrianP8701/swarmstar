from pydantic import BaseModel, Field
from typing import List, Optional

from tree_swarm.swarm.types import NodeEmbryo, BlockingOperation, SpawnOperation


class DecomposeDirectiveModel(BaseModel):
    scrap_paper: Optional[str] = Field(..., 'Scrap paper for notes, planning etc. (optional)')
    subdirectives: Optional[List[str]] = Field(..., description="List of subdirectives to be executed in parallel, if you have no questions.")
    questions: Optional[List[str]] = Field(..., description="List of questions to ask you need answered before decomposition.")
    
system_instructions = (
    'You are given a directive. You have 2 options:\n'
    '1. Ask questions to get more information or clarification of requirements and intentions.\n'
    '2. Decompose the directive into actionable subdirectives that will be executed independently and in parralel. '
    'After those are done, youll generate the next set of subdirectives. I stress that the subdirectives '
    'must be independent and parallel.\n\nChoose one of the options and proceed. Do not ask questions and decompose the directive at the same time.'
    )

def main(node_id: str, message: str) -> BlockingOperation:
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
        operation_type='blocking_operation',
        node_id=node_id,
        blocking_type="openai_instructor_completion",
        args={
            "messages": messages,
            "instructor_model": DecomposeDirectiveModel
        },
        context={
            "directive": message,
            "parent_id": node_id
        },
        next_function_to_call="analyze_output"
    )
    
def analyze_output(directive: str, parent_id: str, completion: DecomposeDirectiveModel) -> SpawnOperation:
    if len(completion.questions) > 0:
        message = f'An agent was tasked with decomposing the directive: \n`{directive}`\n\nBefore decomposing, the agent decided it needs the following questions answered:\n'
        message += '\n'.join(completion.questions)
        
        return SpawnOperation(
            operation_type='spawn',
            node_id=parent_id,
            swarm_commands=[
                NodeEmbryo(
                    action_id='tree_swarm/actions/communication/ask_user_questions',
                    message=message,
                )
            ],
            report=f'The agent tasked with decomposing directives decided to ask the user questions about directive: \n`{directive}`\n\nQuestions:\n' + '\n'.join(completion.questions)
        )
    else:
        return subdirectives_to_swarm_commands(directive, parent_id, completion)

def subdirectives_to_swarm_commands(directive: str, parent_id: str, completion: DecomposeDirectiveModel) -> List[SpawnOperation]:
    subdirectives = completion.subdirectives

    node_embryos = []
    for subdirective in subdirectives:
        node_embryo = NodeEmbryo(
            action_id='tree_swarm/actions/swarm/actions/route_to_action',
            message=subdirective,
        )
        node_embryos.append(node_embryo)
        
        spawn_operation = SpawnOperation(
            operation_type='spawn',
            node_id=parent_id,
            node_embryos=node_embryos,
            report=f'Decomposed directive: \n`{directive}`\n\nInto subdirectives:\n' + '\n'.join(subdirectives)
        )
            
        return spawn_operation
