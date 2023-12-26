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

class Swarm:
    '''
    Create swarm. 
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
            self.population = 0
            self.snapshot_path = snapshot_path
            self.history_path = history_path
            self._load()
            self.is_initialized = True

    def load_goal(self, goal: str, context=None):
        '''
        If your starting a new swarm with an empty snapshot you need to select a goal and context
        '''
        if not self.state['population'] == 0:
            raise ValueError('Create a new swarm to load a new goal')
        if context == None: context = ''
        root_node = Node(id=0, type='route', data={'subtasks': [goal], 'context': context, 'is_parallel': False}, parent=None)
        self.population += 1
        self.lifecycle_queue.put_nowait(('spawn', root_node))

    async def run(self):
        '''
            This is the main function that loops until the swarm completes its goal
        '''
        while True:
            action, node = await self.lifecycle_queue.get() # action can be 'create' or 'terminate'
            try:
                if action == 'spawn':
                    pass
                elif action == 'terminate':
                    pass
                else:
                    raise ValueError(f'Invalid action passed to lifecycle queue: {action}')
                
                result = await self.task_handler.handle_task(node)
            except Exception as error:
                print(error)
            finally:
                self.task_queue.task_done()     
                
    async def save(self, action_type, node: Node):
        self.history.append({
            "action": action_type,
            "node": node.jsonify()
        })
        
        with open(self.history_path, 'w') as file:
            json.dump(self.history, file, indent=4)
            
    '''
    +------------------------ Private methods ------------------------+
    '''        

    async def _spawn_node(self, node):
        '''
        Now you need to save to history the fact that this node was created.
        Save to state the node prior to execution
        Then execute the task
        Then save to state the node after execution
        And save to history the fact that the node was executed
        '''
        
        # A question is, should we bother checkpointing here? Its redundant to have a checkpoint for creation and execution. Just execution is enough. 
        creation_checkpoint = {
            'action': 'spawn',
            'node': node.jsonify()
        }
        self._save_checkpoint(creation_checkpoint)
        self._update_state('spawn', node)
        
        output = await node.execute()
        
        '''
        Output should be:
        {
            'action': 'spawn',
            'node_blueprints': [[type, data]...]
        }
        
        or 
        
        {
            'action': 'terminate'
        }
        '''
        
        # TODO TODO TODO TODO TODO TODO WE ARE WORKING HERE!!!!! TODO TODO TODO TODO TODO TODO
        # first u need to set up the thing that executes the script inside the node
        # Then that node should return the necessary info back here to create or terminate nodes next which happens right here, below.
        pass
    
    def _save_checkpoint(self, checkpoint):
        self.history.append(checkpoint)
        json.dump(self.history, self.history_path, indent=4)
        
    def _update_state(self, action_type: str, node: Node):
        if action_type == 'spawn':
            self.state['nodes'][self.population] = node
            self.population += 1
        elif action_type == 'terminate':
            pass
        else:
            raise ValueError(f'Invalid action type: {action_type}')
        
    def _load(self):
        '''
        Load swarm state, history, and agents
        '''
        self.history = self._load_json_file(self.history_path, [])
        self.state = self._load_json_file(self.snapshot_path, {})

        self.population = self.state.get('population', 0)
        self.task_queue = self.state.get('task_queue', [])

        self.agents = self._load_agents(settings.AGENTS_PATH)        

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