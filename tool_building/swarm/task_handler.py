import json
import traceback
        
class TaskHandler:
    '''This class handles the execution of tasks for nodes. It loads scripts in string form from a JSON file and can execute them'''
    _instance = None

    # Singleton pattern
    def __new__(cls, scripts_file=None):
        if cls._instance is None:
            cls._instance = super(TaskHandler, cls).__new__(cls)
            cls._instance.__init__(scripts_file)
        return cls._instance

    def __init__(self, scripts_file=None):
        if not hasattr(self, 'is_initialized'):
            self.activated_scripts = {}
            self.scripts_file = scripts_file
            self._load_scripts(scripts_file)
            self.is_initialized = True

    async def execute(self, node):
        script_name = node.type
        if script_name not in self.activated_scripts:
            self._activate_script(script_name)
        if script_name in self.activated_scripts:
            try:
                output =  await self.activated_scripts[script_name](**node.data)
                return output
            except TypeError as e:
                print(f"Error calling function {script_name}: {e}")
                traceback.print_exc()
        else:
            print(f"Function {script_name} is not available.")
    '''
    +------------------------ Private methods ------------------------+
    '''  
    
    def _load_scripts(self, scripts_file):
        try:
            with open(scripts_file, 'r') as file:
                self.scripts_as_strings = json.load(file)
        except FileNotFoundError:
            print(f"Functions file {scripts_file} not found.")
            self.scripts_as_strings = {}

    def _activate_script(self, script_name):
        if script_name in self.scripts_as_strings:
            exec(self.scripts_as_strings[script_name]['script'], globals())
            self.activated_scripts[script_name] = globals()[script_name]

    def _save_script(self, script_name, script_as_string, description, language):
        new_script = {
            'script': script_as_string,
            'description': description,
            'language': language
        }
        self.scripts_as_strings[script_name] = new_script
        with open(self.scripts_file, 'w') as file:
            json.dump(self.scripts_as_strings, file, indent=4)