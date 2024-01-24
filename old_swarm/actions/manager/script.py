import sys
import json
import asyncio
sys.path.insert(0, '/Users/brianprzezdziecki/Code/Agent_Swarm_Experiments')

from old_swarm.core.oai_agent import OAI_Agent
from old_swarm.settings import Settings
from old_swarm.utils.actions.validate_action_args import validate_action_args
settings = Settings()

async def manager(directive: str):
    with open('swarm/actions/manager/tool.json', 'r') as file:
        agent_blueprint = json.load(file)
    
    tools = agent_blueprint['manager']['tools']
    instructions = agent_blueprint['manager']['instructions']
    tool_choice =  {"type": "function", "function": {"name": "break_down_directive"}}
    manager = OAI_Agent(instructions, tools, tool_choice)
    
    broken_down_directive = await manager.chat(directive)
    subdirectives = broken_down_directive['arguments']['subtasks']
            
    node_blueprints = []
    for subtask in subdirectives:
        node_blueprints.append({'type': 'action_router', 'data': {'directive': subtask}})

    lifecycle_command = {'action': 'spawn', 'node_blueprints': node_blueprints}
    report = {
        'message': f'Given the directive "{directive}", the manager chose the subtasks "{subdirectives}"',
        'subdirectives': subdirectives
    }
    return {'report': report, 'lifecycle_command': lifecycle_command}

# async def manager_with_old_tool(directive: str):
#     with open('swarm/actions/manager/tool.json', 'r') as file:
#         agent_blueprint = json.load(file)
    
#     tools = agent_blueprint['manager']['tools']
#     instructions = agent_blueprint['manager']['instructions']
#     tool_choice =  {"type": "function", "function": {"name": "break_down_directive"}}
#     manager = OAI_Agent(instructions, tools, tool_choice)
    
#     while True:
#         broken_down_directive = await manager.chat(directive)
#         agent_has_questions = broken_down_directive['arguments'].get('do_you_have_questions', False)

#         if agent_has_questions:
#             question = broken_down_directive['arguments']['questions']
#             user_input = input(f"Questions: {question}\n\nGoal: {directive}\n\n")
#             directive = f'{directive}\n\nQuestion: {question} \n\nUser answer: {user_input}'
#         else:
#             subtasks = broken_down_directive['arguments']['subtasks']
#             break
            
#     node_blueprints = []
#     for subtask in subtasks:
#         node_blueprints.append({'type': 'action_router', 'data': {'directive': subtask}})

#     return {'action': 'spawn', 'node_blueprints': node_blueprints}

def main(args):
    try:
        results = asyncio.run(manager(args['directive']))
        print(json.dumps(results))  # Convert dict to JSON and print
    except Exception as e:
        raise RuntimeError(f"Script execution failed: {str(e)}")

if __name__ == "__main__":
    schema = {
        "directive": str
    }
    args_dict = validate_action_args(schema)
    main(args_dict)