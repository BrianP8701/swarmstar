from openai_config import get_openai_client
import asyncio
from functools import partial

client = get_openai_client()

class Agent:
    def __init__(self, instructions, tools):
        self.instructions = instructions
        self.tools = tools
        
    async def chat(self, message, tool_choice="auto"):
        loop = asyncio.get_running_loop()
        messages = [{"role": "system","content": self.instructions},{"role": "user","content": message}]
        
        def create_sync(model, messages, tools, tool_choice, temperature):
            return client.chat.completions.create(model=model, messages=messages, tools=tools, tool_choice=tool_choice, temperature=temperature)
        func = partial(create_sync, "gpt-4-1106-preview", messages, self.tools, tool_choice, 0.0)
        
        completion = await loop.run_in_executor(None, func)
        return self.get_tool_outputs(completion)

    def get_tool_outputs(self, completion):
        tools_dict = {}
        for tool_call in completion.choices[0].message.tool_calls:
            tools_dict[tool_call.function.name] = tool_call.function.arguments
        return tools_dict