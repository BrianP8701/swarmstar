from swarm.task_handler import TaskHandler
import asyncio
from task import Task
import json
from swarm.agent import Agent

class Swarm:
    def __init__(self, conversation_path):
        self.tools = {}
        self.conversation_path = conversation_path
        self.task_queue = asyncio.Queue()
        self.task_handler = TaskHandler('tool_building/config/functions.json')
        with open('tool_building/config/agents.json') as f:
            self.agent_schemas = json.load(f)
        self.agents = {}
        self.agents['head_agent'] = Agent(self.agent_schemas['head_agent']['instructions'], self.agent_schemas['head_agent']['tools'])
        
    async def start(self, goal):
        initialize_swarm = Task('break_down_goal', {'goal': goal, 'swarm': self})
        print('starting swarm\n')
        self.task_queue.put_nowait(initialize_swarm)
        while True:
            task = await self.task_queue.get()
            try:
                # Process the task (API call, database operation, etc.)
                print('got here')
                result = await self.task_handler.handle_task(task)
                print(result)
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
                
# def break_down_goal(goal, swarm):
#     swarm.agents['head_agent'] = Agent(swarm.agent_schemas['head_agent']['instructions'], swarm.agent_schemas['head_agent']['tools'])
#     subtasks = swarm.agents['head_agent'].chat(goal)
#     return subtasks