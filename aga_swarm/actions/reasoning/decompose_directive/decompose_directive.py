from pydantic import BaseModel, Field
import traceback
from typing import List

from aga_swarm.swarm.types import NodeIO, Swarm, SwarmCommand, LifecycleCommand, NodeIO, BlockingOperation
from aga_swarm.swarm_utils.ai.openai_instructor import completion


class DecomposeDirective(BaseModel):
    subdirectives: List[str] = Field(..., description="Decompose the directive into subdirectives")


def main(swarm: Swarm, node_id: str, directive: str) -> NodeIO:

        
    system_instructions = '''You play a pivotal role in navigating complex goals across various levels in domains like software 
    development, engineering, and research. Your operations within this multi-tiered system 
    include:\n\nIterative Goal Interpretation and Decomposition: In the swarm hierarchy, you'll 
    handle goals at different completion stages. Your primary task is to break down these goals 
    into smaller, actionable sub-goals. This process involves one critical pathway:\n\nDirect 
    Subgoal Generation: Based on the existing information, proceed to generate and output a list 
    of subgoals.\n\nSubgoal Contextualization and Assignment: When formulating subgoals, ensure 
    each one is bundled with all relevant and available information. Strive for a balance between 
    providing enough detail for effective downstream execution and maintaining overall resource 
    efficiency.\n\nParallel Goal Output: Focus on identifying subgoals that can be pursued 
    immediately and in parallel, independent of other tasks. Your output should exclusively 
    list these parallelizable subgoals, omitting any that are sequential or reliant on the 
    completion of others. Sequential or dependent goals will be formulated in subsequent phases 
    once the immediate parallel tasks are completed.\n\nDynamic Routing and Task Delegation: Your 
    formulated subgoals are routed to the 'router' agent. This agent is responsible for assigning 
    tasks to suitable subagents, who will execute actions like coding, further goal decomposition, 
    research and more.\n\nCost-Efficiency and Operations: Uphold cost-efficiency at every management 
    level. Ensure that the subgoals you provide are detailed yet concise, adhering to the context 
    window and budgetary constraints.'''
    
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
