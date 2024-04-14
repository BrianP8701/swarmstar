"""
Decide which memory node to navigate to to answer a question

prompt: route_question_prompt + 
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


system_prompt = ASK_QUESTIONS_INSTRUCTIONS + """

"""

user_prompt = """

"""

constants = []
message = ASK_QUESTIONS_INSTRUCTIONS + system_prompt + "\n\n\n" + user_prompt

if constants:
    message += "\n\n" + "The following constants were provided:\n" + "\n".join(constants)

messages = [{"role": "system", "content": message}]
output = asyncio.run(instructor.completion(messages, Model))

print(output)









output_string = output.model_dump_json(indent=4)

txt_file = '/Users/brianprzezdziecki/swarmstar_world/swarmstar/tests/history.txt'

with open(txt_file, 'w') as file:
    file.write("\n\n\n\n\n\n" + message + "\n\n" + output_string + "\n\n\n\n\n")

