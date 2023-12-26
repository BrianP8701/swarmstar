'''
Same functions as in functions.json, but just easier to read here.
'''

'''
+----------------- manager -----------------+
'''
from swarm.swarm import Swarm
async def break_down_goal(goal, context):
    swarm = Swarm()
    manager = swarm.agents['manager']
    broken_down_goal = await manager.chat(f'Context to understand the goal: {context}\n\n\n The goal: {goal}')

    node_blueprints = []
    for subgoal in broken_down_goal['arguments']['subtasks']:
        data = {
            'goal': subgoal,
            'context': broken_down_goal['arguments']['context']
        }
        node_blueprints.append({'type': 'route', 'data': data})
        if broken_down_goal['arguments']['is_parallel']:
            break
    return node_blueprints
'''
+----------------- router -----------------+
'''
from swarm.swarm import Swarm
async def route(goal):
    swarm = Swarm()
    router_agent = swarm.agents['router']
    options = ['break_down_goal', 'write_text', 'write_python', 'retrieve_info', 'ask_user_for_help']
    
    action_index = await router_agent.chat(goal)
    action_index = action_index['arguments']['next_action']
    node_blueprints = [{'type': options[action_index-1], 'data': {'goal': goal}}]
            
    return {'action': 'create', 'node_blueprints': node_blueprints}

'''
+----------------- write_python -----------------+
'''

            
'''
+----------------- save_python_code -----------------+
'''      
from swarm.memory.save_code import save_python_code 
async def save_python_code(code_type, python_code, name, description):
    save_python_code(code_type, python_code, name, description)