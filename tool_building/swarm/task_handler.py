import json

class TaskHandler:
    def __init__(self, functions_file):
        self.activated_functions = {}
        self.functions_file = functions_file
        self.load_functions()

    def load_functions(self):
        try:
            with open(self.functions_file, 'r') as file:
                self.functions_as_strings = json.load(file)
        except FileNotFoundError:
            print(f"Functions file {self.functions_file} not found.")
            self.functions_as_strings = {}

    async def activate_function(self, function_name):
        if function_name in self.functions_as_strings:
            exec(self.functions_as_strings[function_name], globals())
            self.activated_functions[function_name] = globals()[function_name]

    async def handle_task(self, task):
        function_name = task.task_type
        print('got here gang')
        if function_name not in self.activated_functions:
            await self.activate_function(function_name)

        if function_name in self.activated_functions:
            try:
                # Unpacking the dictionary 'data' as keyword arguments
                print('got here too')
                result =  await self.activated_functions[function_name](**task.data)
                return result
            except TypeError as e:
                print(f"Error calling function {function_name}: {e}")
        else:
            print(f"Function {function_name} is not available.")

    def save_function(self, function_name, function_str):
        self.functions_as_strings[function_name] = function_str
        with open(self.functions_file, 'w') as file:
            json.dump(self.functions_as_strings, file, indent=4)
    
    async def enqueue_items(self, tasks):
        for task in tasks:
            await self.task_queue.put(task)