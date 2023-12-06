from swarm.swarm import Swarm
async def route_subtasks(broken_down_goal):
    swarm = Swarm()
    subtasks = broken_down_goal['subtasks']
    is_parallel = broken_down_goal['is_parallel']
    context = broken_down_goal['context']
    task_list = ['break_down_goal', 'write_python', 'retrieve_info', 'ask_user_for_help']
    
    def route_to_task_from_action_index(action_index, subtask):
        data = {'task': subtask, 'context': context}
        next_task = Task(task_list[action_index], data)
        swarm.task_queue.put_nowait(next_task)
        
    def messagify(subtask):
        return f"Context to understand the task: {context}\n\n\n The task. Decide what we should do next to accomplish this: {subtask}"
    
    if not is_parallel:
        action_index = await swarm.agents['subtask_router_agent'].chat(messagify(subtasks[0]))['arguments']['action_index']
        route_to_task_from_action_index(action_index-1, subtasks[0])
    else:
        for subtask in subtasks:
            action_index = await swarm.agents['subtask_router_agent'].chat(messagify(subtask))['arguments']['action_index']
            route_to_task_from_action_index(action_index-1, subtask)