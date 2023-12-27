import json

class TaskHandler:
    '''This class handles the execution of tasks for nodes. It loads scripts in string form from a JSON file and can execute them'''
    _instance = None

    # Singleton pattern
    def __new__(cls, scripts_file=None):
        if cls._instance is None:
            cls._instance = super(TaskHandler, cls).__new__(cls)
            cls._instance.__init__(scripts_file)
        return cls._instance

    def __init__(self, functions_file=None):
        if not hasattr(self, 'is_initialized'):
            self.activated_functions = {}
            self._load_functions(functions_file)
            self.is_initialized = True

    async def execute(self, node):
        function_name = node.task_type
        if function_name not in self.activated_functions:
            await self._activate_function(function_name)

        if function_name in self.activated_functions:
            try:
                output =  await self.activated_functions[function_name](**node.data)
                return output
            except TypeError as e:
                print(f"Error calling function {function_name}: {e}")
        else:
            print(f"Function {function_name} is not available.")
    
    '''
    +------------------------ Private methods ------------------------+
    '''  
    
    def _load_functions(self, functions_file):
        try:
            with open(functions_file, 'r') as file:
                self.functions_as_strings = json.load(file)
        except FileNotFoundError:
            print(f"Functions file {functions_file} not found.")
            self.functions_as_strings = {}

    async def _activate_function(self, function_name):
        if function_name in self.functions_as_strings:
            exec(self.functions_as_strings[function_name], globals())
            self.activated_functions[function_name] = globals()[function_name]

    def _save_function(self, function_name, function_str):
        self.functions_as_strings[function_name] = function_str
        with open(self.functions_file, 'w') as file:
            json.dump(self.functions_as_strings, file, indent=4)