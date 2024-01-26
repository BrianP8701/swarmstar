import os
import json
import openai
import sys
import json

sys.path.insert(0, '/Users/brianprzezdziecki/Code/autonomous-general-agent-swarm/old_swarm')
from openai_config import get_openai_client

client = get_openai_client()
print('gera')

class OAI_Agent:
    def __init__(self, instructions, tools, tool_choice="auto"):
        self.instructions = instructions
        self.tools = tools
        if tool_choice == "auto" or type(tool_choice) == dict:
            self.tool_choice = tool_choice
        elif type(tool_choice) == str:
            self.tool_choice = {"type": "function", "function": {"name": tool_choice}}
        else:
            raise ValueError(f"Invalid tool_choice type: {type(tool_choice)}")
        
    def chat(self, message):
        
        messages = [{"role": "system", "content": self.instructions},{"role": "user", "content": message}]
        print('\n\n\n\n\n')
        print(messages)
        print('\n\n\n\n\n')
        try:
            completion = client.chat.completions.create(model="gpt-4-1106-preview", messages=messages, tools=self.tools, tool_choice=self.tool_choice, temperature=0.0, response_format={ "type": "json_object" }, seed=69) # hahaha 69 funny number
        except Exception as e:
            print(f"Exception occurred: {e}")
            return
        extracted_tool_output = self.get_tool_output(completion)
        return extracted_tool_output

    def get_tool_output(self, completion):
        tool_output = {}
        for tool_call in completion.choices[0].message.tool_calls:
            tool_output['function_name'] = tool_call.function.name
            tool_output['arguments'] = json.loads(tool_call.function.arguments)
        return tool_output
def get_file_paths(folder_path):
    file_paths = []
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.endswith('.py') and file != '__init__.py':
                full_path = os.path.join(root, file)
                file_paths.append(full_path)
    return file_paths

def check_files_in_json(file_paths, json_path):
    with open(json_path, 'r') as json_file:
        data = json.load(json_file)
        existing_paths = data.keys()
        return [file_path for file_path in file_paths if print(file_path) or file_path in existing_paths]

def cut(file_paths):
    cut_paths = []
    for path in file_paths:
        cut_path = path.split('/actions', 1)[-1]
        cut_path = 'actions' + cut_path
        cut_paths.append(cut_path)
    return cut_paths

def create_action(cut_paths, json_path):
    with open(json_path, 'r') as json_file:
        data = json.load(json_file)
    for action_id in cut_paths:
        
        action_metadata = data[action_id]
        prompt = (
            'Follow the given JSON schema. You need to create a function that accomplishes the function described filling in the given blank slate:\n'
            f'{action_metadata["description"]}\n'
            f'Function name: {action_metadata["name"]}\n'
            f'Parameters: {action_metadata["input_schema"]}\n'
            f'Output: {action_metadata["output_schema"]}\n'
            f'Please ensure the script includes a function named {action_metadata["name"]}. Additionally, the script must contain a main section that calls {action_metadata["name"]}() using the provided input schema.'
        )

        tool = {
            "type": "function",
            "function": {
                "name": "write_function",
                "arguments": json.dumps({
                    "script": action_id,
                    "input_schema": action_metadata["input_schema"],
                    "output_schema": action_metadata["output_schema"]
                })
            }
        }
        tools = [
            {
                "type": "function",
                "function": {
                    "name": "write_function",
                    "description": "Write the python function with the given input and output schema.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "script": {
                                "type": "string",
                                "description": "The full and complete code as described in the instructions."
                            }
						}
                    },
                    "required": [
                        "script"
                    ]
                }
            }
        ]
        
        agent = OAI_Agent(instructions = prompt, tools = tools, tool_choice = {"type": "function", "function": {"name": "write_function"}})
        response = agent.chat('write the script')
        print(response)
        script = response['arguments']['script']
        path = os.path.join('/Users/brianprzezdziecki/Code/autonomous-general-agent-swarm/autonomous_general_agent_swarm', action_id)
        # save the script to the path {action_id}
        with open(path, 'w') as file:
            file.write(script)
            
    # pass


folder_path = '/Users/brianprzezdziecki/Code/autonomous-general-agent-swarm/autonomous_general_agent_swarm/actions/data'
json_path = 'autonomous_general_agent_swarm/actions/action_space.json'

print('\n\n\n\n')



file_paths = get_file_paths(folder_path)
cut_paths = cut(file_paths)
create_action(cut_paths, json_path)