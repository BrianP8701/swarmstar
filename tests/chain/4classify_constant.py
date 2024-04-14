"""
Classifying a constant

prompt: classify_constant_prompt + constant_type_options + constant

no questions can be asked
"""
from swarmstar.utils.ai import Instructor
import asyncio

from typing import Optional
from pydantic import BaseModel, Field


instructor = Instructor()

class Model(BaseModel):
    constant_type_index: Optional[int] = Field(None, description="The index of the constant type to classify the constant as. None if the constant is not a constant.")


system_prompt = """
You need to identify what type of constant this is. If it doesen't match any of the options, output None.
"""

constant_types = ["github_link", "file_path", "openai_api_key"]

user_prompt = """
https://github.com/BrianP8701/swarmstar
"""

message = system_prompt + "\n" + "\n".join([str(i) + " " + constant_type for i, constant_type in enumerate(constant_types)]) + "\n\n" + user_prompt

messages = [{"role": "system", "content": message}]
output = asyncio.run(instructor.completion(messages, Model))

print(output)









output_string = output.model_dump_json(indent=4)

txt_file = '/Users/brianprzezdziecki/swarmstar_world/swarmstar/tests/history.txt'

with open(txt_file, 'w') as file:
    file.write("\n\n\n\n\n\n" + message + "\n\n" + output_string + "\n\n\n\n\n")

