import json
from swarm.core.oai_agent import OAI_Agent
from swarm.settings import Settings
from swarm.utils.user_input import get_user_input
import copy

settings = Settings()

async def memory_router(directive: str):
    '''
    The action router decides what action to take next given a string, the "directive"
    }
    '''
    with open('swarm/actions/memory_router/tool.json') as f:
        router_schema = json.load(f)
    tool_blueprint = router_schema['memory_router']['tools'][0]
    instructions = router_schema['memory_router']['instructions']

    with open(settings.MEMORY_SPACE_PATH) as f:
        memory_space = json.load(f)
        
    searching_memory_space = True
    options = _extract_options(memory_space)
    path = []
    
    while searching_memory_space:
        # Let LLM choose where to go in the action_space
        tool_blueprint_copy = copy.deepcopy(tool_blueprint)
        action_router = _update_router(options, tool_blueprint_copy, instructions)
        action_router_output = await action_router.chat(directive)
        action_index = action_router_output['arguments'].get('action_index', None)
        
        # Get assistance from the user if needed
        need_user_assistance = action_router_output['arguments'].get('help', False)
        if need_user_assistance or action_index == None: action_index = _get_user_input(directive, options)

        # Continue to traverse action space if you are in a folder. Exit if you are in an action.
        path.append(options[action_index]['key'])
        subspace = _traverse_path(memory_space, path)
        if subspace['type'] == 'folder':
            options = _extract_options(subspace)
        elif subspace['type'] == 'action':
            searching_memory_space = False
        else:
            raise ValueError(f"Invalid type in action space. Expected 'folder' or 'action'.\n\nPath: {path}\n\n")
    
    node_blueprints = [{'action_path': path, 'data': {'directive': directive}}]
    return {'action': 'spawn', 'node_blueprints': node_blueprints}

def _update_router(options, tool, instructions):
    tool['function']['parameters']['properties']['action_index']['description'] += str(options)
    tool['function']['parameters']['properties']['action_index']['enum'] = list(range(len(options)))

    tool_choice = {"type": "function", "function": {"name": tool['function']['name']}}
    
    return OAI_Agent(instructions, [tool], tool_choice)

def _extract_options(space):
    result = {}
    i = 0
    for key, value in space.items():
        if isinstance(value, dict) and key not in ['type', 'description']:
            result[i] = {
                "key": key,
                "description": value.get('description', '')
            }
            i += 1  
    return result

def _get_user_input(directive, options):
    while True:
        user_input = get_user_input(f"The action router needs help:\n\nDirective:\n{directive}\n\nPlease choose the index of the agent this goal should be routed to: {options}")
        if user_input.isdigit():
            user_number = int(user_input)
            if 0 <= user_number <= len(options):
                print(f"You chose the number: {user_number}")
                return user_number
            else:
                print("Number out of range. Please try again. Don't select user_assistance again.")
        else:
            print("Invalid input. Please enter a number.")

def _traverse_path(action_space, path):
    current_space = action_space
    for key in path:
        current_space = current_space[key]
    
    return current_space

def main(directive: str):
    return memory_router(directive)