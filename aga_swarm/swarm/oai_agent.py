from openai import OpenAI
from typing import Union, List, Dict
from pydantic import validate_arguments
from pydantic import BaseModel
from typing import Union, List, Dict
from openai import OpenAI

from aga_swarm.swarm.types import SwarmID

class OAI_Agent(BaseModel):
    instructions: str
    tools: List[Dict]
    openai_key: str
    tool_choice: Union[str, dict] = "auto"

    def __init__(self, **data):
        super().__init__(**data)
        self.client = OpenAI(self.openai_key)
        
        if self.tool_choice == "auto" or isinstance(self.tool_choice, dict):
            self.tool_choice = self.tool_choice
        elif isinstance(self.tool_choice, str):
            self.tool_choice = {"type": "function", "function": {"name": self.tool_choice}}
        else:
            raise ValueError(f"Invalid tool_choice type: {type(self.tool_choice)}")

    @validate_arguments
    def chat(self, message: str) -> dict:
        messages = [{"role": "system", "content": self.instructions},{"role": "user", "content": message}]
        try:
            completion = self.client.chat.completions.create(model="gpt-4-1106-preview", messages=messages, tools=self.tools, tool_choice=self.tool_choice, temperature=0.0, response_format={ "type": "json_object" }, seed=69) # hahaha 69 funny number
        except Exception as e:
            return e
   
        return self.get_tool_output(completion)

    def get_tool_output(self, completion):
        return completion.choices[0].message.tool_calls[0]['arguments']
