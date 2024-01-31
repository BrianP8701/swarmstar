from openai import OpenAI
from typing import Union, List, Dict, Any
from pydantic import validate_call, BaseModel
import json

class OAI_Agent(BaseModel):
    instructions: str
    tools: List[Dict]
    openai_key: str
    tool_choice: Union[str, dict] = "auto"
    client: Any = None

    def __init__(self, **data):
        super().__init__(**data)
        self.client = OpenAI(api_key=self.openai_key)
        
        if self.tool_choice == "auto" or isinstance(self.tool_choice, dict):
            self.tool_choice = self.tool_choice
        elif isinstance(self.tool_choice, str):
            self.tool_choice = {"type": "function", "function": {"name": self.tool_choice}}
        else:
            raise ValueError(f"Invalid tool_choice type: {type(self.tool_choice)}")

    @validate_call
    def chat(self, message: str) -> dict:
        messages = [{"role": "system", "content": self.instructions},{"role": "user", "content": message}]
        try:
            completion = self.client.chat.completions.create(model="gpt-4-1106-preview", messages=messages, tools=self.tools, tool_choice=self.tool_choice, temperature=0.0, response_format={ "type": "json_object" }, seed=69) # hahaha 69 funny number
        except Exception as e:
            raise e
   
        return self._get_tool_output(completion)

    def _get_tool_output(self, completion) -> dict:
        return json.loads(completion.choices[0].message.tool_calls[0].function.arguments)
