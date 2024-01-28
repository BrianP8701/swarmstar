import json
import sys
import asyncio
sys.path.insert(0, '/Users/brianprzezdziecki/Code/Agent_Swarm_Experiments')

from old_swarm.core.oai_agent import OAI_Agent
from old_swarm.settings import Settings
from old_swarm.utils.actions.validate_action_args import validate_action_args

settings = Settings()

async def manager_supervisor(directive: str):
    '''
    The action router decides what action to take next given a string, the "directive"
    '''
    with open('swarm/actions/core/manager_supervisor/tool.json') as f:
        schema = json.load(f)
    tools = schema['manager_supervisor']['tools']
    instructions = schema['manager_supervisor']['instructions'] 
    
    manager_supervisor = OAI_Agent(tools, instructions, 'manager_supervisor')
    manager_supervisor_output = await manager_supervisor.chat(directive)
    try:
        directive_accomplished = manager_supervisor_output['arguments']['directive_accomplished']
    except KeyError:
        raise ValueError(f"manager_supervisor did not output 'action_index'.\n\nOutput: {manager_supervisor_output}")

    if directive_accomplished:
        lifecycle_command = {'action': 'terminate', 'node_blueprints': []}
    else:
        node_blueprints = [{'type': 'manager', 'data': {'directive': directive}}]
        lifecycle_command = {'action': 'spawn', 'node_blueprints': node_blueprints}
        
    report = {
        'message': f'Given the directive "{directive}", the manager supervisor chose to {lifecycle_command["action"]}'
    }
    return {'report': report, 'lifecycle_command': lifecycle_command}

def main(args):
    try:
        results = asyncio.run(manager_supervisor(args['directive']))
        print(json.dumps(results))  # Convert dict to JSON and print
    except Exception as e:
        raise RuntimeError(f"Script execution failed: {str(e)}")

if __name__ == "__main__":
    schema = {
        "directive": str
    }
    args_dict = validate_action_args(schema)
    main(args_dict)