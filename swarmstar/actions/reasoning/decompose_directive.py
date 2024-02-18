from pydantic import BaseModel, Field
from typing import List, Optional

from swarmstar.swarm.types import NodeEmbryo, BlockingOperation, SpawnOperation, SwarmState, SwarmConfig


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
        operation_type='blocking_operation',
        node_id=node_id,
        blocking_type="openai_instructor_completion",
        args={
            "messages": messages,
            "instructor_model": DecomposeDirectiveModel
        },
        context={
            "swarm": swarm,
            "directive": message,
            "parent_id": node_id
        },
        next_function_to_call="analyze_output"
    )
    
def analyze_output(swarm: SwarmConfig, directive: str, parent_id: str, completion: DecomposeDirectiveModel) -> SpawnOperation:
    if len(completion.questions) > 0:
        message = f'An agent was tasked with decomposing the directive: \n`{directive}`\n\nBefore decomposing, the agent decided it needs the following questions answered:\n'
        message += '\n'.join(completion.questions)
        
        spawn_operation = SpawnOperation(
            operation_type='spawn',
            node_id=parent_id,
            node_embryo=NodeEmbryo(
                    action_id='swarmstar/actions/communication/ask_user_questions',
                    message=message
                )
        )
        swarm_state = SwarmState(swarm=swarm)
        node = swarm_state[parent_id]
        node.report = (
            f'The agent tasked with decomposing directives decided to ask the user questions '
            'about directive: \n`{directive}`\n\nQuestions:\n' + '\n'.join(completion.questions)
        )
        swarm_state.update_node(node)
        return spawn_operation
    else:
        return subdirectives_to_swarm_commands(swarm, directive, parent_id, completion)

def subdirectives_to_swarm_commands(swarm: SwarmConfig, directive: str, parent_id: str, completion: DecomposeDirectiveModel) -> List[SpawnOperation]:
    subdirectives = completion.subdirectives
    
    spawn_operations = []
    for subdirective in subdirectives:
        node_embryo = NodeEmbryo(
            action_id='swarmstar/actions/swarm/actions/route_action',
            message=subdirective
        )        
        spawn_operations.append(SpawnOperation(
            operation_type='spawn',
            node_id=parent_id,
            node_embryos=node_embryo,
        ))
        
    return spawn_operations
