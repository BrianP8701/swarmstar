from old_swarm.openai_config import get_async_openai_client
import json

client = get_async_openai_client()

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
        
    async def chat(self, message):
        messages = [{"role": "system", "content": self.instructions},{"role": "user", "content": message}]
        try:
            completion = await client.chat.completions.create(model="gpt-4-1106-preview", messages=messages, tools=self.tools, tool_choice=self.tool_choice, temperature=0.0, response_format={ "type": "json_object" }, seed=69) # hahaha 69 funny number
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