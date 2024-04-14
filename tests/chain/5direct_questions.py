"""
directing questions to oracle, browser or user

we dont direct questions initially actually
because the answer might already be in the user folder, or stored in the repo or docs.
we always want to first search the memory system and then as a last resort browse the web or ask the user.

No questions
"""
from swarmstar.utils.ai import Instructor
from swarmstar.utils.ai.prompts import ASK_QUESTIONS_INSTRUCTIONS
import asyncio

from typing import List, Optional
from pydantic import BaseModel, Field



question_object = {
    "shared_context_for_questions": "The goal is to add web browsing actions to a complex swarm system and to help write and build out comprehensive documentation for the project. The project's documentation is currently out of date and not comprehensive. The expert, original creator, and active maintainer of the project is available for specific questions.",
    "questions": [
        "Can you provide a high-level overview of the current architecture of the swarm system?",
        "What specific web browsing actions do you want to add to the swarm?",
        "Are there any existing components or modules in the swarm system that can be extended or reused for web browsing capabilities?",
        "What documentation format do you prefer (e.g., markdown, reStructuredText, wiki) and where should the documentation be hosted?",
        "Do you have any coding standards or guidelines that should be followed when contributing to the project?",
        "What is the current process for testing new features or changes in the swarm system?"
    ]
}


instructor = Instructor()

class Model(BaseModel):
    List[int] = Field(None, description="List of which source to direct question to for each question")


system_prompt = ASK_QUESTIONS_INSTRUCTIONS + """
For each question, select the best source to direct the question to:
0: Memory System (Oracle)
1. Web Browser
2. User

If it might be possible to derive the answer from the memory system, say by reading code or documentation, choose 0.
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

