from swarm.task_handler import TaskHandler
import asyncio
from swarm.node import Node
import json
import os
from swarm.agent import Agent
from settings import Settings

settings = Settings() # For config paths

class Swarm:
    '''
    Swarm params:
    task_queue: asyncio.Queue of (node, task) tuples
        The swarm follows a async producer-consumer pattern
    task_handler: TaskHandler
        Because some "tasks" might be saved as strings we have this one unified object to execute all fucntions
    agents: dict 
        Contains agent names with their instructions and tools.
    history_path: str
        JSON path to save history of swarm. This provides an easy way to visualize, debug and trace the swarms actions and choices
    snapshot_path: str
        JSON path to snapshot of swarm. This allows you to save and resume execution of a swarm state on seperate runs.
    goal: str
    context: str
        If your starting a new swarm with an empty snapshot you need to select a goal and context
    '''
    _instance = None

    # Singleton pattern
    def __new__(cls, save_path=None):
        if cls._instance is None:
            cls._instance = super(Swarm, cls).__new__(cls)
            cls._instance.__init__(save_path)
        return cls._instance

    def __init__(self, snapshot_path=None, history_path=None, goal=None, context=None):
        if not hasattr(self, 'is_initialized'):
            self.task_queue = asyncio.Queue()
            self.goal = goal
            self.context = context
            self.task_handler = TaskHandler(settings.FUNCTIONS_PATH, self)            
            self.history_path = history_path
            self.population = 1
            if not os.path.exists(history_path):
                self.history = []
            else:
                with open(history_path, 'r') as file:
                    self.history = json.load(file)
            
            self.agents = {}
            with open(settings.AGENTS_PATH) as f:
                self.agent_schemas = json.load(f)
            for agent in self.agent_schemas:
                tool_choice = {"type": "function", "function": {"name": self.agent_schemas[agent]['tools'][0]['function']['name']}}
                self.agents[agent] = Agent(self.agent_schemas[agent]['instructions'], self.agent_schemas[agent]['tools'], tool_choice)
            self.initialize(snapshot_path)
            self.is_initialized = True

    async def run(self):
        '''
            This is the main function that loops until the swarm completes its goal
        '''
        while True:
            node = await self.task_queue.get()
            try:
                result = await self.task_handler.handle_task(node)
            except Exception as error:
                print(error)
            finally:
                self.task_queue.task_done()

    # TODO: 

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
    
    def initialize(self, snapshot_path):
        '''
        Align swarm state with snapshot. If snapshot is empty, create a root node with the given goal
        '''
        if not os.path.exists(snapshot_path):
            self.state = {}
        else:
            with open(snapshot_path, 'r') as file:
                self.state = json.load(file)
          
        if self.state == {}:
            if self.goal == None: #TODO wtf is a key error what is the relevant error here?
                raise KeyError("Theres no fucking goal L bozo")
            root_node = Node(0, 'route_task', {'subtasks': [self.goal], 'context': self.context, 'is_parallel': False})
            self.task_queue.put_nowait(root_node)
            self.state['nodes'][0] = root_node
            self.save('create_node', root_node)
        else:
            self.population = self.state['population']
            self.task_queue = self.state['task_queue']          
                
    def save(self, action_type, node: Node):
        self.history.append({
            "action": action_type,
            "node": node.jsonify()
        })
        
        with open(self.history_path, 'w') as file:
            json.dump(self.history, file, indent=4)