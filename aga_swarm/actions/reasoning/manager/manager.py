import json
from pydantic import validate_arguments

from aga_swarm.swarm.types import NodeOutput, SwarmID, SwarmCommand, LifecycleCommand, NodeReport, NodeOutput, NodeStatus
from aga_swarm.swarm.oai_agent import OAI_Agent

def manager(directive: str, swarm_id: SwarmID) -> NodeOutput:
    with open('aga_swarm/actions/reasoning/manager/tool.json', 'r') as file:
        manager_blueprint = json.load(file)
    
    tools = manager_blueprint['manager']['tools']
    instructions = manager_blueprint['manager']['instructions']
    manager = OAI_Agent(instructions=instructions, tools=tools, tool_choice="break_down_directive", openai_key=swarm_id.configs.openai_key)
    
    try:
        subdirectives = manager.chat(directive)['subdirectives']
    except Exception as e:
        return NodeOutput(
            lifecycle_command=LifecycleCommand.NODE_FAILURE,
            swarm_commands=[],
            report=e
        )

    swarm_commands = []
    for subdirective in subdirectives:
        swarm_command = SwarmCommand(
            action_id='aga_swarm/actions/swarm/action_router/action_router.py',
            params = {
                'directive': subdirective,
                'swarm_id': swarm_id
            }
        )
        swarm_commands.append(swarm_command)
    
    return NodeOutput(
        lifecycle_command=LifecycleCommand.SPAWN,
        swarm_commands=swarm_commands,
        report=f'Directive: {directive}\n\nSubdirectives:\n' + '\n'.join(subdirectives)
    )

@validate_arguments
def main(directive: str, swarm_id: SwarmID) -> NodeOutput:
    return manager(directive, swarm_id)