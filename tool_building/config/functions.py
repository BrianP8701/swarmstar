'''
Same functions as in functions.json, but just easier to read here.
'''

'''
+----------------- break_down_goal -----------------+
'''
from swarm.swarm import Swarm
from task import Task
async def break_down_goal(goal):
    swarm = Swarm()
    head_agent = swarm.agents['head_agent']
    
    broken_down_goal = await head_agent.chat(goal)
    next_task = Task('route_task', broken_down_goal['arguments'])
    swarm.task_queue.put_nowait(next_task)
    swarm.save(swarm.save_path, broken_down_goal['arguments'])

'''
+----------------- route_task -----------------+
'''
from swarm.swarm import Swarm
from task import Task
async def route_task(subtasks, context, is_parallel):
    swarm = Swarm()
    router_agent = swarm.agents['router_agent']
    task_list = ['break_down_goal', 'write_text', 'write_python', 'retrieve_info', 'ask_user_for_help']
    save_message = {}
    
    def route_to_task_from_action_index(action_index, subtask):
        goal = {'goal': f'Context to understand the task: {context}\n\n\n The task: {subtask}'}
        next_task = Task(task_list[action_index], goal)
        swarm.task_queue.put_nowait(next_task)
        save_message[subtask] = task_list[action_index]
        
    def messagify(subtask):
        return f"Context to understand the task: {context}\n\n\n The task. Decide what we should do next to accomplish this: {subtask}"
    
    if not is_parallel:
        action_index = await router_agent.chat(messagify(subtasks[0]))
        action_index = action_index['arguments']['next_action']
        route_to_task_from_action_index(action_index-1, subtasks[0])
    else:
        for subtask in subtasks:
            action_index = await router_agent.chat(messagify(subtask))
            action_index = action_index['arguments']['next_action']
            route_to_task_from_action_index(action_index-1, subtask)
            
    swarm.save(swarm.save_path, save_message)
            
'''
+----------------- write_python -----------------+
'''
from swarm.swarm import Swarm
from swarm.agent import Agent
from task import Task
async def write_python(goal):
    swarm = Swarm()
    python_agent: Agent = swarm.agents['write_python_agent']
    
    tool_output = await python_agent.chat(goal)
    code_type = tool_output['arguments']['code_type']
    python_code = tool_output['arguments']['python_code']
    name = tool_output['arguments']['name']
    description = tool_output['arguments']['description']
    
    next_task = Task('save_python_code', tool_output['arguments'])
    swarm.task_queue.put_nowait(next_task)
    save_message = f'The code we wrote to solve: {goal} \n{name}\nCode Type (0: Function, 1: Class, 2: Script) - {code_type}\n{python_code}\n{description}'
    swarm.save(swarm.save_path, save_message)
            
'''
+----------------- save_python_code -----------------+
'''      
from swarm.memory.save_code import save_python_code 
async def save_python_code(code_type, python_code, name, description):
    save_python_code(code_type, python_code, name, description)