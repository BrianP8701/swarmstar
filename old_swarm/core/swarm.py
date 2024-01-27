import asyncio
import traceback

from old_swarm.core.node import Node
from old_swarm.settings import Settings
from old_swarm.utils.actions.executor import execute_node

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
        '''
        This is the main function that loops until the swarm completes its goal.
        '''
        try:
            self.is_running = True
            await self._main()
        except KeyboardInterrupt:
            self._stop()
            await self._main()


    '''
    +------------------------ Private methods ------------------------+
    '''        

    async def _main(self):
        self.running_tasks = set()

        while self.is_running:
            node = await self.lifecycle_queue.get()
            if node == 'STOP':
                break
            try:
                task = asyncio.create_task(self._execute_node(node))
                self.running_tasks.add(task)
                task.add_done_callback(self.running_tasks.discard)
            except Exception as error:
                print(error)
            finally:
                self.lifecycle_queue.task_done()
        
        # When the swarm is stopped, wait for all running tasks to finish and save state
        if self.running_tasks:
            await asyncio.gather(*self.running_tasks)
    
    def _stop(self):
        '''
            This is called when the user presses ctrl+c
        '''
        self.is_running = False
        self.lifecycle_queue.put_nowait('STOP')

    async def _execute_node(self, node: Node):
        try:
            node_output = await execute_node(node)
            lifecycle_command = node_output['lifecycle_command']
            report = node_output['report']
            node.lifecycle_command = lifecycle_command
            node.report = report
        except Exception as error:
            print(f'Error executing node {node.id}: {error}')
            traceback.print_exc()

        if lifecycle_command['action'] == 'spawn': # Create and add children to lifecycle queue
            for node_blueprint in lifecycle_command['node_blueprints']:
                child = self._spawn_node(node_blueprint)
                node.children.append(child)
                child.parent = node
        elif lifecycle_command['action'] == 'terminate':
            self._terminate_node(node)
        else:
            raise ValueError(f'Invalid action type from executing node: {lifecycle_command["action"]}')

    def _terminate_node(self, node: Node):
        '''
            When a node terminates, the following steps are taken:
            1. Traverse up the parent chain to find a manager or root node.
            2. If a manager node is found, verify if all its children have terminated.
            3. If all children are terminated:
                a. Check for the presence of a manager_supervisor among the children.
                b. If a manager_supervisor exists, proceed to terminate the manager node.
                c. If no manager_supervisor is found, spawn one as a child of the manager node.
        '''
        current_node = node
        while current_node.parent is not None and current_node.parent.type != 'manager':
            current_node.alive = False
            current_node = self.nodes[current_node.parent.id]
        
        if current_node.parent is None:
            self._stop()
            return
        
        manager_node = self.nodes[current_node.parent.id]
        
        all_children_terminated = all(child.alive == False for child in manager_node.children)
        if all_children_terminated:
            manager_supervisor_exists = any(child.type == 'manager_supervisor' for child in manager_node.children)
            if manager_supervisor_exists:
                manager_node.alive = False
                self._terminate_node(manager_node)
            else:
                updated_directive = f'{manager_node.data["directive"]}\n\nWe have already accomplished the following sub-directives:\n{manager_node.report["subdirectives"]}\n\n'
                manager_supervisor_blueprint = {'type': 'manager_supervisor', 'data': {'directive': updated_directive}}
                manager_supervisor = self._spawn_node(manager_supervisor_blueprint)
                manager_node.children.append(manager_supervisor)
                manager_supervisor.parent = manager_node
    
    def _spawn_node(self, node_blueprint):
        node = Node(id=self.state['population'], type=node_blueprint['type'], data=node_blueprint['data'])
        self.state['population'] += 1
        self.nodes[node.id] = node
        self.lifecycle_queue.put_nowait(node)
        return node
