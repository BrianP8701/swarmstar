import asyncio
import json
import os
import traceback

from swarm.core.node import Node
from swarm.core.oai_agent import OAI_Agent
from swarm.settings import Settings
from swarm.utils.actions.executor import execute_node

settings = Settings() # For config paths

class Swarm:
    '''
        If you are creating a new swarm you need to initialize it with a goal by calling load_goal()

        To run the swarm call run()
    '''
    _instance = None

    # Singleton pattern
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Swarm, cls).__new__(cls)
            cls._instance.__init__()
        return cls._instance

    def __init__(self):
        if not hasattr(self, 'is_initialized'):
            self.is_initialized = True
            self.state = {'population': 0}
            self.nodes = {}
            self.lifecycle_queue = asyncio.Queue()

    def load_directive(self, directive: str):
        '''
            If your starting a new swarm with an empty snapshot 
            you need to initialize the swarm with a goal
        '''
        if not self.state['population'] == 0:
            raise ValueError('Create a new swarm to load a new goal')
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
            output = await execute_node(node)
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

    def _spawn_node(self, node_blueprint):
        
        node = Node(id=self.state['population'], type=node_blueprint['type'], data=node_blueprint['data'])
        self.state['population'] += 1
        self.nodes[node.id] = node
        self.lifecycle_queue.put_nowait(('execute', node))
        return node

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
