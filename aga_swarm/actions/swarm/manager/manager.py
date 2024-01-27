import json
from pydantic import validate_arguments

from aga_swarm.swarm.types import NodeOutput, SwarmID
from aga_swarm.swarm.oai_agent import OAI_Agent

@validate_arguments
def manager(directive: str, swarm_id: SwarmID) -> NodeOutput:
    with open('aga_swarm/actions/swarm/manager/tool.json', 'r') as file:
        manager_blueprint = json.load(file)
    
    tools = manager_blueprint['manager']['tools']
    instructions = manager_blueprint['manager']['instructions']
    manager = OAI_Agent(instructions=instructions, tools=tools, tool_choice="break_down_directive", swarm_id=swarm_id)
    
    try:
        subdirectives = manager.chat(directive)['subdirectives']
    except Exception as e:
        node_report = {
            'success': False,
            'error': str(e)
        }
        return {'node_report': node_report, 'swarm_commands': []}
    # subdirectives = broken_down_directive['subdirectives']

    swarm_commands = []
    
    for subdirective in subdirectives:
        swarm_command = {
            'lifecycle_command': 'spawn',
            'action': {
                'action_id': 'aga_swarm/actions/swarm/action_router/action_router.py',
                'params': {
                    'directive': subdirective,
                    'swarm_id': swarm_id
                }
            },
            'swarm_id': swarm_id
        }
        swarm_commands.append(swarm_command)
    
    node_report = {
        'success': True,
        'message': f'Given the directive "{directive}", the manager chose the subtasks "{subdirectives}"'
    }
    return {'node_report': node_report, 'swarm_commands': []}

@validate_arguments
def main(directive: str, swarm_id: SwarmID) -> NodeOutput:
    return manager(directive, swarm_id)