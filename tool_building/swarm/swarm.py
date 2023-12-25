from swarm.task_handler import TaskHandler
import asyncio
from swarm.node import Node
import json
import os
from swarm.agent import Agent
from settings import Settings
from pydantic import BaseModel
from typing import Optional, List

settings = Settings() # For config paths

class Swarm(BaseModel):
    '''
    Create swarm. 
    Call initialize() to align swarm state with snapshot. If snapshot is empty, create a root node with the given goal
    The only inputs to swarm are snapshot and history path
    You have two choices:
        - Create a new swarm with a goal and context
        - Resume a swarm from a snapshot
    
    Lifecycle queue is the asyncio queue that handles creation and termination of nodes
    It takes in a tuple of (action, node) with actions being 'create_node' or 'terminate_node'
    
    If a node is created execute it. If a node is being terminated, the swarm will terminate it
    '''
    _instance = None

    # Singleton pattern
    def __new__(cls, snapshot_path=None, history_path=None):
        if cls._instance is None:
            cls._instance = super(Swarm, cls).__new__(cls)
            cls._instance.__init__(snapshot_path, history_path)
        return cls._instance

    def __init__(self, snapshot_path=None, history_path=None):
        if not hasattr(self, 'is_initialized'):
            self.lifecycle_queue = asyncio.Queue()
            self.population = 1
            self.snapshot_path = snapshot_path
            self.history_path = history_path
            self.load()
            self.is_initialized = True

    def load(self):
        '''
        Load swarm state, history, and agents
        '''
        # Load history from file or initialize to empty list if file doesn't exist
        self.history = self._load_json_file(self.history_path, [])

        # Load state from file or initialize to empty dict if file doesn't exist
        self.state = self._load_json_file(self.snapshot_path, {})

        # Update population and task_queue if state is not empty
        if self.state:
            self.population = self.state.get('population', 0)
            self.task_queue = self.state.get('task_queue', [])

        # Load agents
        self.agents = self._load_agents(settings.AGENTS_PATH)

    def load_goal(self, goal: str, context=None):
        '''
        Align swarm state with snapshot. If starting from scratch, provide a goal to initiate the swarm
        '''
        if not self.state == {}:
            raise ValueError('Cannot initiate a swarm when snapshot is not empty. Create a new swarm instead.')
        if context == None: context = ''
        root_node = Node(0, 'route', {'subtasks': [goal], 'context': context, 'is_parallel': False})
        self.lifecycle_queue.put_nowait(('create_node', root_node))
        
        # TODO MOVE THIS TO THE LOOP THAT HANDLES LIFECYCLE QUEUE
        self.state['nodes'][0] = root_node
        self.save('create_node', root_node)

    
    async def run(self):
        '''
            This is the main function that loops until the swarm completes its goal
        '''
        while True:
            action, node = await self.lifecycle_queue.get()
            try:
                result = await self.task_handler.handle_task(node)
            except Exception as error:
                print(error)
            finally:
                self.task_queue.task_done()     
                
    def save(self, action_type, node: Node):
        self.history.append({
            "action": action_type,
            "node": node.jsonify()
        })
        
        with open(self.history_path, 'w') as file:
            json.dump(self.history, file, indent=4)
            
    def _load_json_file(self, file_path, default_value):
        if os.path.exists(file_path):
            with open(file_path, 'r') as file:
                return json.load(file)
        return default_value

    def _load_agents(self, agents_path):
        agents = {}
        with open(agents_path) as f:
            agent_schemas = json.load(f)
        for agent in agent_schemas:
            tool_choice = {"type": "function", "function": {"name": agent_schemas[agent]['tools'][0]['function']['name']}}
            agents[agent] = Agent(agent_schemas[agent]['instructions'], agent_schemas[agent]['tools'], tool_choice)
        return agents