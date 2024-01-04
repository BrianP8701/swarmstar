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
    
    while True:
        broken_down_goal = await manager.chat(goal)
        agent_has_questions = broken_down_goal['arguments']['do_you_have_questions']
        question = broken_down_goal['arguments']['question']

        if agent_has_questions:
            user_input = input(f"Questions: {question}\n\nGoal: {goal}\n\n")
            goal = f'{goal}\n\nQuestion: {question} \n\nUser answer: {user_input}'
        else:
            subgoals = broken_down_goal['arguments']['subgoals']
            break
            
    node_blueprints = []
    for subgoal in subgoals:
        node_blueprints.append({'type': 'router', 'data': {'goal': subgoal}})

    return {'action': 'spawn', 'node_blueprints': node_blueprints}
'''
+----------------- router -----------------+
'''
from swarm.swarm import Swarm
async def router(goal):
    swarm = Swarm()
    router_agent = swarm.agents['router']
    options = ['user_assistance', 'python_coder', 'manager', 'writer', 'retrieval']
    
    agent_index = await router_agent.chat(goal)
    agent_index = agent_index['arguments']['agent_index']
    
    if agent_index == 0: # User assistance
        while True:
            user_input = input(f"The router agent needs assistance routing this goal:\n\n{goal}\n\nPlease choose the index of the agent this goal should be routed to: {options}")
            if user_input.isdigit():
                user_number = int(user_input)
                if 1 <= user_number <= len(options):
                    print(f"You chose the number: {user_number}")
                    agent_index = user_number
                    break
                else:
                    print("Number out of range. Please try again. Don't select user_assistance again.")
            else:
                print("Invalid input. Please enter a number.")
                
    node_blueprints = [{'type': options[agent_index], 'data': {'goal': goal}}]
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
    
    # Gather all relevant context
    code_analyst = swarm.agents['code_analyst']
    while True:
        questions = await code_analyst.chat(goal)
        analyst_has_questions = questions['arguments']['do_you_have_questions']
        questions = questions['arguments']['questions']

        if analyst_has_questions:
            user_input = input(f"\n\nGoal: {goal}\n\nQuestions: {questions}\n")
            goal = f'{goal}\n\nQuestions: {questions} \n\nUser answer: {user_input}'
        else: 
            break

    # Write code
    python_coder = swarm.agents['python_coder']
    code = await python_coder.chat(goal)
    code_type = ['function', 'class', 'script', 'other']
    packet = {
        'language': 'python',
        'code_type': code_type[code['arguments']['code_type']],
        'code': code['arguments']['python_code'],
        'description': code['arguments']['description'],
        'dependencies': code['arguments']['dependencies']
    }

    file_name = settings.SYNTHETIC_CODE_PATH
    with open(file_name, 'r') as file:
        data = json.load(file)
    data[code['arguments']['name']] = packet
    with open(file_name, 'w') as file:
        json.dump(data, file, indent=4)

    return {'action': 'terminate', 'node_blueprints': []}    