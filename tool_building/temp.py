from swarm.task_handler import TaskHandler
from task import Task
from swarm.swarm import Swarm

task_handler = TaskHandler('tool_building/config/functions.json')
task_handler.activate_function('break_down_goal')
swarm = Swarm('')
task = Task('break_down_goal', {'goal': 'Create a new revolutionary CRM for real estate agents that takes advantage of chatgpt', 'swarm': swarm})
subtasks = task_handler.handle_task(task)
print(subtasks)