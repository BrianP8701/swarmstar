import asyncio
from swarm.core.node import Node
import json
import os
from swarm.core.oai_agent import Agent
from settings import Settings
import traceback
from swarm.core.executor import execute

settings = Settings() # For config paths

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

    def load_goal(self, directive: str):
        '''
            If your starting a new swarm with an empty snapshot you need to initialize the swarm with a goal
        '''
        if not self.state['population'] == 0:
            raise ValueError('Create a new swarm to load a new goal')
        if context == None: context = ''
        node_blueprint = {'type': 'action_router', 'data': {'directive': directive}}
        self._spawn_node(node_blueprint)

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
                if action == 'execute':
                    # Create a task for spawn_node and add it to running_tasks
                    task = asyncio.create_task(self._execute_node(node))
                    self.running_tasks.add(task)
                    # Optionally, add a callback to remove the task from running_tasks when it's done
                    task.add_done_callback(self.running_tasks.discard)
                elif action == 'terminate':
                    # TODO TODO TODO TODO Handle termination TODO TODO TODO TODO
                    pass
                else:
                    raise ValueError(f'Invalid action passed to lifecycle queue: {action}')

            except Exception as error:
                print(error)
            finally:
                self.lifecycle_queue.task_done()  
        
        # When the swarm is stopped, wait for all running tasks to finish and save state
        if self.running_tasks:
            await asyncio.gather(*self.running_tasks) 
        self._save_state()

    '''
    +------------------------ Private methods ------------------------+
    '''        

    def _stop(self):
        '''
            This is called when the user presses ctrl+c
        '''
        self.is_running = False

    async def _execute_node(self, node: Node):
        '''
        Execute node
        If node returns spawn, spawn and add children to lifecycle queue
        If node returns terminate, inititate termination process
        '''
        try:
            output = await execute(node)
            node.output = output
        except Exception as error:
            print(f'Error executing node {node.id}: {error}')
            traceback.print_exc()

        if output['action'] == 'spawn': # Create and add children to lifecycle queue
            for node_blueprint in output['node_blueprints']:
                child = self._spawn_node(node_blueprint)
                node.children.append(child)
                child.parent = node
        elif output['action'] == 'terminate':
            pass
        else:
            raise ValueError(f'Invalid action type from executing node: {output["action"]}')
        
        checkpoint = {
            'action': 'spawn',
            'node': node.jsonify()
        }
        self._save_checkpoint(checkpoint)

    def _spawn_node(self, node_blueprint):
        node = Node(id=self.state['population'], type=node_blueprint['type'], data=node_blueprint['data'])
        self.state['population'] += 1
        self.nodes[node.id] = node
        self.lifecycle_queue.put_nowait(('execute', node))
        return node

    def _save_checkpoint(self, checkpoint):
        self.history.append(checkpoint)
        os.makedirs(os.path.dirname(self.history_path), exist_ok=True)
        with open(self.history_path, 'w') as history:
            json.dump(self.history, history, indent=4)

    def _save_state(self):
        self.state['lifecycle_queue'] = self.lifecycle_queue_to_list()
        for node in self.nodes:
            self.state['nodes'][node.id] = node.jsonify()
        os.makedirs(os.path.dirname(self.snapshot_path), exist_ok=True)
        with open(self.snapshot_path, 'w') as snapshot:
            json.dump(self.state, snapshot, indent=4)

    def _load(self):
        '''
        Initialize swarm from snapshot or create new swarm
        '''
        self.history = self._load_json_file(self.history_path, [])
        self.state = self._load_json_file(self.snapshot_path, {'population': 0, 'nodes': {}, 'lifecycle_queue': []})
        
        if self.state['population'] == 0: # initialize swarm with empty state
            self.lifecycle_queue = asyncio.Queue()
            self.nodes = {}
        else:
            self._load_swarm_from_snapshot()
            
        self.agents = self._load_agents(settings.AGENTS_PATH)        

    def _load_swarm_from_snapshot(self):
        # Load nodes
        for node_id in self.state['nodes']: # Create all nodes without parent or children relationships
            jsonified_node = self.state['nodes'][node_id]
            self.nodes[node_id] = Node(node_id, jsonified_node['task_type'], jsonified_node['input_data'])
        for node_id in self.state['nodes']: # Create parent and children relationships
            jsonified_node = self.state['nodes'][node_id]
            node = self.nodes[node_id]
            parent_id = jsonified_node['parent_id']
            node.parent = self.nodes[parent_id] if parent_id is not None else None
            for child_id in jsonified_node['children_ids']:
                node.children.append(self.nodes[child_id])
        
        # Load lifecycle queue
        for action, node_id in self.state['lifecycle_queue']: # Create lifecycle queue
            node = self.nodes[node_id]
            self.lifecycle_queue.put_nowait((action, node))

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

    async def lifecycle_queue_to_list(self):
        '''
            Returns a list of tuples of the form (action, node_id). This will clear the lifecycle queue. Only used when the swarm is stopped to save lifecycle queue to snapshot
        '''
        result = []
        queue = self.lifecycle_queue
        while not queue.empty():
            action, node = await queue.get()
            result.append([action, node.id])
        return result

    '''
    +------------------------ Testing methods ------------------------+
    '''       

    def offline_testing(self):
        pass