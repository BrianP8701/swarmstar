from swarm.core.swarm import Swarm
async def manager(goal):
    swarm = Swarm()
    manager = swarm.agents['manager']
    
    while True:
        broken_down_goal = await manager.chat(goal)
        agent_has_questions = broken_down_goal['arguments']['do_you_have_questions']

        if agent_has_questions:
            question = broken_down_goal['arguments']['question']
            user_input = input(f"Questions: {question}\n\nGoal: {goal}\n\n")
            goal = f'{goal}\n\nQuestion: {question} \n\nUser answer: {user_input}'
        else:
            subgoals = broken_down_goal['arguments']['subgoals']
            break
            
    node_blueprints = []
    for subgoal in subgoals:
        node_blueprints.append({'type': 'router', 'data': {'goal': subgoal}})

    return {'action': 'spawn', 'node_blueprints': node_blueprints}