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
    broken_down_goal = await swarm.agents['head_agent'].chat(goal)
    next_task = Task('route_subtasks', broken_down_goal['arguments'])
    swarm.task_queue.put_nowait(next_task)

'''
+----------------- route_subtasks -----------------+
'''
from swarm.swarm import Swarm
from task import Task
async def route_subtasks(subtasks, context, is_parallel):
    swarm = Swarm()
    task_list = ['break_down_goal', 'write_text', 'write_python', 'retrieve_info', 'ask_user_for_help']
    
    def route_to_task_from_action_index(action_index, subtask):
        goal = f'Context: {context}\n\n\nGoal: {subtask}'
        data = {'goal': goal}
        next_task = Task(task_list[action_index], data)
        swarm.task_queue.put_nowait(next_task)
        
    def messagify(subtask):
        return f"Context to understand the task: {context}\n\n\n The task. Decide what we should do next to accomplish this: {subtask}"
    
    if not is_parallel:
        action_index = await swarm.agents['subtask_router_agent'].chat(messagify(subtasks[0]))
        action_index = action_index['arguments']['next_action']
        route_to_task_from_action_index(action_index-1, subtasks[0])
    else:
        for subtask in subtasks:
            action_index = await swarm.agents['subtask_router_agent'].chat(messagify(subtask))
            action_index = action_index['arguments']['next_action']
            route_to_task_from_action_index(action_index-1, subtask)
            
            
            
            