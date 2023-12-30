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
    options = ['manager', 'write_text', 'write_python', 'retrieve_info', 'ask_user_for_help']
    
    action_index = await router_agent.chat(goal)
    action_index = action_index['arguments']['next_action']
    node_blueprints = [{'type': options[action_index-1], 'data': {'goal': goal}}]
            
    return {'action': 'spawn', 'node_blueprints': node_blueprints}

'''
+----------------- write_python -----------------+
'''

            
'''
+----------------- save_python_code -----------------+
'''      
from swarm.memory.save_code import save_python_code 
async def save_python_code(code_type, python_code, name, description):
    save_python_code(code_type, python_code, name, description)