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
            self.functions_as_strings = {}

    def activate_function(self, function_name):
        if function_name in self.functions_as_strings:
            exec(self.functions_as_strings[function_name], globals())
            self.activated_functions[function_name] = globals()[function_name]

    def handle_task(self, task):
        function_name = task.task_type
        if function_name not in self.activated_functions:
            self.activate_function(function_name)

        if function_name in self.activated_functions:
            try:
                # Unpacking the dictionary 'data' as keyword arguments
                return self.activated_functions[function_name](**task.data)
            except TypeError as e:
                print(f"Error calling function {function_name}: {e}")
        else:
            print(f"Function {function_name} is not available.")

    def save_function(self, function_name, function_str):
        self.functions_as_strings[function_name] = function_str
        with open(self.functions_file, 'w') as file:
            json.dump(self.functions_as_strings, file, indent=4)