import json
from task import Task

class TaskHandler:
    '''This class handles the execution of tasks. It loads functions from a file and executes them when needed.'''
    def __init__(self, functions_file, swarm):
        self.activated_functions = {}
        self.load_functions(functions_file)
        self.swarm = swarm
        self.task_queue = swarm.task_queue

    def load_functions(self, functions_file):
        try:
            with open(functions_file, 'r') as file:
                self.functions_as_strings = json.load(file)
        except FileNotFoundError:
            print(f"Functions file {functions_file} not found.")
            self.functions_as_strings = {}

    async def activate_function(self, function_name):
        if function_name in self.functions_as_strings:
            exec(self.functions_as_strings[function_name], globals())
            self.activated_functions[function_name] = globals()[function_name]

    async def handle_task(self, task):
        function_name = task.task_type
        if function_name not in self.activated_functions:
            await self.activate_function(function_name)

        if function_name in self.activated_functions:
            try:
                tool_output =  await self.activated_functions[function_name](**task.data)
                return tool_output
            except TypeError as e:
                print(f"Error calling function {function_name}: {e}")
        else:
            print(f"Function {function_name} is not available.")

    def save_function(self, function_name, function_str):
        self.functions_as_strings[function_name] = function_str
        with open(self.functions_file, 'w') as file:
            json.dump(self.functions_as_strings, file, indent=4)