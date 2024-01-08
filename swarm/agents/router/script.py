from swarm.core.swarm import Swarm
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