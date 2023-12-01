from swarm.task_handler import TaskHandler
import asyncio
from types import Task
import json

with open('/Users/brianprzezdziecki/Code/Agent_Swarm_Experiments/tool_building/constants.json', 'r') as file:
    constants = json.load(file)


class Swarm:
    def __init__(self, conversation_path):
        self.tools = {}
        self.agents = {}
        self.conversation_path = conversation_path
        self.task_queue = asyncio.Queue()
        self.task_handler = TaskHandler(constants['functions_config_path'])
    
    async def start(self, goal):
        initialize_swarm = Task('initialize_swarm', {'goal': goal})
        self.task_queue.put_nowait(initialize_swarm)
        while True:
            task = await self.task_queue.get()
            try:
                # Process the task (API call, database operation, etc.)
                result = await self.task_handler.handle_task(task)
                # Handle the result (save to database, further processing, etc.)
            except Exception as error:
                # Handle errors
                print(error)
            finally:
                self.task_queue.task_done()
        
    def execute_function(self, function_name):
        for tool in self.tools:
            if hasattr(tool, function_name):
                getattr(tool, function_name)()