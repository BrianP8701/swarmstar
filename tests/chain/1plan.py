"""
generate sequential plan given directive/goal

prompt: ask_questions_prompt + plan_prompt + goal
"""
from swarmstar.utils.ai import Instructor
from swarmstar.utils.ai.prompts import ASK_QUESTIONS_INSTRUCTIONS
import asyncio

from typing import List, Optional
from pydantic import BaseModel, Field


instructor = Instructor()

class Model(BaseModel):
    shared_context_for_questions: Optional[str] = Field(None, description="Context shared with all questions if you have questions, otherwise None")
    questions: Optional[List[str]] = Field(None, description="List of questions to ask if you have questions, otherwise None")

    plan: Optional[List[str]] = Field(None, description="List of steps to take to accomplish the task")

system_prompt = ASK_QUESTIONS_INSTRUCTIONS + """
Create a plan to accomplish the goal.

GOAL:

"""

user_prompt = """
Hi i want u to help me with my project. I want u to add web browsing actions to my swarm. my systems quite complex
and the docs are out of date and also not that comprehensive. so in the process of adding the web browsing actions
also help write and build out good docs. im the expert, original creator and active maintainer of the project so
feel free to ask me specific questions about the project :)
"""

constants = ["https://github.com/BrianP8701/swarmstar"]
message = system_prompt + "\n\n\n" + user_prompt

if constants:
    message += "\n\n" + "The following constants were provided:\n" + "\n".join(constants)

messages = [{"role": "system", "content": message}]
output = asyncio.run(instructor.completion(messages, Model))

print(output)









output_string = output.model_dump_json(indent=4)

txt_file = '/Users/brianprzezdziecki/swarmstar_world/swarmstar/tests/history.txt'

with open(txt_file, 'w') as file:
    file.write("\n\n\n\n\n\n" + message + "\n\n" + output_string + "\n\n\n\n\n")

