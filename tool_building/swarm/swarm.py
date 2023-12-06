from swarm.task_handler import TaskHandler
import asyncio
from task import Task
import json
from swarm.agent import Agent

class Swarm:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Swarm, cls).__new__(cls)
            # Initialize the instance here if needed
            cls._instance.__init__()
        return cls._instance

    def __init__(self):
        if not hasattr(self, 'is_initialized'):
            self.tools = {}
            self.task_queue = asyncio.Queue()
            self.task_handler = TaskHandler('tool_building/config/functions.json', self)
            with open('tool_building/config/agents.json') as f:
                self.agent_schemas = json.load(f)
            self.agents = {}
            for agent in self.agent_schemas:
                self.agents[agent] = Agent(agent['instructions'], agent['tools'], agent['tools']['function']['name'])
            self.is_initialized = True
        
    async def start(self, goal):
        initialize_swarm = Task('break_down_goal', {'goal': goal})
        print('starting swarm\n')
        self.task_queue.put_nowait(initialize_swarm)
        while True:
            task = await self.task_queue.get()
            print(task)
            try:
                result = await self.task_handler.handle_task(task)
                print(result)
            except Exception as error:
                print(error)
            finally:
                self.task_queue.task_done()