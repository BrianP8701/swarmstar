'''
Every script should output a dictionary with one of the following structure:
{
    'action': 'create children' or 'terminate',
    'node_blueprints': list of node blueprints to be created
}   
'''

'''
+----------------- manager -----------------+
'''
from swarm.swarm import Swarm
async def manager(goal):
    swarm = Swarm()
    manager = swarm.agents['manager']
    broken_down_goal = await manager.chat(goal)

    node_blueprints = []
    for subgoal in broken_down_goal['arguments']['subtasks']:
        node_blueprints.append({'type': 'router', 'data': {'goal': subgoal}})
        if not broken_down_goal['arguments']['is_parallel']:
            break
    return {'action': 'spawn', 'node_blueprints': node_blueprints}
'''
+----------------- router -----------------+
'''
from swarm.swarm import Swarm
async def router(goal):
    swarm = Swarm()
    router_agent = swarm.agents['router']
    options = ['manager', 'write_text', 'python_coder', 'retrieve_info', 'ask_user_for_help']
    
    action_index = await router_agent.chat(goal)
    action_index = action_index['arguments']['next_action']
    node_blueprints = [{'type': options[action_index-1], 'data': {'goal': goal}}]
            
    return {'action': 'spawn', 'node_blueprints': node_blueprints}

'''
+----------------- python_coder -----------------+
'''
from swarm.swarm import Swarm
from settings import Settings
import json
settings = Settings() # For config paths

async def python_coder(goal):
    swarm = Swarm()
    python_agent = swarm.agents['python_coder']
    code = await python_agent.chat(goal)
    
    code_type = ['function', 'class', 'script']
    packet = {
        'language': 'python',
        'code_type': code_type[code['arguments']['code_type']],
        'code': code['arguments']['python_code'],
        'description': code['arguments']['description']
    }

    file_name = settings.SYNTHETIC_CODE_PATH
    with open(file_name, 'r') as file:
        data = json.load(file)
    data[code['arguments']['name']] = packet
    with open(file_name, 'w') as file:
        json.dump(data, file, indent=4)

    return {'action': 'terminate', 'node_blueprints': []}    
            
'''
+----------------- save_python_code -----------------+
'''      
from swarm.memory.save_code import save_python_code 
async def save_python_code(code_type, python_code, name, description):
    save_python_code(code_type, python_code, name, description)