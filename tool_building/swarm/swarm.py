import asyncio
from swarm.node import Node
import json
import os
from swarm.agent import Agent
from settings import Settings
from swarm.task_handler import TaskHandler
from pydantic import BaseModel
from typing import Optional, List

settings = Settings() # For config paths
task_handler = TaskHandler(settings.NODE_SCRIPTS_PATH)

class Swarm:
    '''
        If you are creating a new swarm you need to initialize it with a goal by calling load_goal()
        
        To run the swarm call run() 
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
            self.snapshot_path = snapshot_path
            self.history_path = history_path
            self._load()
            self.is_initialized = True

    def load_goal(self, goal: str, context=None):
        '''
            If your starting a new swarm with an empty snapshot you need to initialize the swarm with a goal
        '''
        if not self.state['population'] == 0:
            raise ValueError('Create a new swarm to load a new goal')
        if context == None: context = ''
        root_node = Node(id=0, type='route', data={'subtasks': [goal], 'context': context, 'is_parallel': False}, parent=None)
        self.population += 1
        self.lifecycle_queue.put_nowait(('spawn', root_node))

    async def run(self):
        try:
            self.is_running = True
            await self.main()
        except KeyboardInterrupt:
            self._stop()
            await self.main()
            
    async def main(self):
        '''
        This is the main function that loops until the swarm completes its goal.
        '''
        self.running_tasks = set()

        while self.is_running:
            action, node = await self.lifecycle_queue.get() # action can be 'spawn' or 'terminate'
            try:
                if action == 'spawn':
                    # Create a task for spawn_node and add it to running_tasks
                    task = asyncio.create_task(self._spawn_node(node))
                    self.running_tasks.add(task)
                    # Optionally, add a callback to remove the task from running_tasks when it's done
                    task.add_done_callback(self.running_tasks.discard)
                elif action == 'terminate':
                    # Handle termination
                    pass
                else:
                    raise ValueError(f'Invalid action passed to lifecycle queue: {action}')

            except Exception as error:
                print(error)
            finally:
                self.lifecycle_queue.task_done()  
        
        # When the swarm is stopped, wait for all running tasks to finish
        if self.running_tasks:
            await asyncio.gather(*self.running_tasks) 

    '''
    +------------------------ Private methods ------------------------+
    '''        

    def _stop(self):
        '''
            This is called when the user presses ctrl+c
        '''
        self.is_running = False
        
    async def _spawn_node(self, node: Node):
        '''
        Execute node
        If node returns spawn, spawn and add children to lifecycle queue
        If node returns terminate, inititate termination process
        '''
        
        output = await task_handler.execute_node(node)
        node.output = output
        
        if output['action'] == 'create children': # Create and add children to lifecycle queue
            for node_blueprint in output['node_blueprints']:
                child = Node(id=self.population, type=node_blueprint[0], data=node_blueprint[1], parent=node)
                self.population += 1
                node.children.append(child)
                self.lifecycle_queue.put_nowait(('spawn', child))
                self._update_state('add', child)
        elif output['action'] == 'terminate':
            pass
        else:
            raise ValueError(f'Invalid action type from executing node: {output["action"]}')
        
        checkpoint = {
            'action': 'spawn',
            'node': node.jsonify()
        }
        self._save_checkpoint(checkpoint)
    
    def _save_checkpoint(self, checkpoint):
        self.history.append(checkpoint)
        json.dump(self.history, self.history_path, indent=4)
        
    def _update_state(self, action_type: str, node: Node):
        if action_type == 'add':
            self.state['nodes'][node.id] = node
            self.state['population'] += 1
        elif action_type == 'delete':
            pass
        else:
            raise ValueError(f'Invalid action type: {action_type}')
        json.dump(self.state, self.snapshot_path, indent=4)
        
    def _load(self):
        '''
        Initialize swarm from snapshot or create new swarm
        '''
        self.history = self._load_json_file(self.history_path, [])
        self.state = self._load_json_file(self.snapshot_path, {'population': 0, 'nodes': {}, 'lifecycle_queue': asyncio.Queue()})

        self.population = self.state.get('population')
        self.lifecycle_queue = self.state.get('lifecycle_queue')

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