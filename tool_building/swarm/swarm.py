from swarm.task_handler import TaskHandler
import asyncio
from task import Task
import json
import os
from swarm.agent import Agent
from settings import Settings

settings = Settings() # For config paths

class Swarm:
    '''
    
    '''
    _instance = None

    # Singleton pattern
    def __new__(cls, save_path=None):
        if cls._instance is None:
            cls._instance = super(Swarm, cls).__new__(cls)
            cls._instance.__init__(save_path)
        return cls._instance

    def __init__(self, save_path=None):
        if not hasattr(self, 'is_initialized'):
            self.tools = {}
            self.task_queue = asyncio.Queue()
            self.task_handler = TaskHandler(settings.FUNCTIONS_PATH, self)
            self.save_path = save_path
            with open(settings.AGENTS_PATH) as f:
                self.agent_schemas = json.load(f)
            self.agents = {}
            for agent in self.agent_schemas:
                tool_choice = {"type": "function", "function": {"name": self.agent_schemas[agent]['tools'][0]['function']['name']}}
                self.agents[agent] = Agent(self.agent_schemas[agent]['instructions'], self.agent_schemas[agent]['tools'], tool_choice)
            self.is_initialized = True

    async def start(self, goal):
        self.task_queue.put_nowait(Task('break_down_goal', {'goal': goal}))
        self.save(self.save_path, f'Goal: {goal}')
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

    async def test(self, task):
        print('\n\nStarting swarm\n\n')
        self.task_queue.put_nowait(task)
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
                
    def save(self, json_path, value):
        if not os.path.exists(json_path):
            data = {}
        else:
            with open(json_path, 'r') as file:
                data = json.load(file)

        if 'len' not in data:
            data['len'] = 0
        
        data[data['len']] = value
        data['len'] += 1
        
        with open(json_path, 'w') as file:
            json.dump(data, file, indent=4)