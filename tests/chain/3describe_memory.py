"""
Generating the short description of the data to save this memory.

prompt: describe_chunk_prompt + chunk_string

No questions
No instructor

maybe sometimes what we have to do is not let the system generate the description. if we know what we're saving pretty well, just manually send it.
"""
from swarmstar.utils.ai import OpenAI
import asyncio



openai = OpenAI()

system_prompt = """
Your saving data to memory. This prompt is reused on every memory save, so at the time of writing, I'm not exactly aware of what you're saving.
However what matters is this. The memory system is a file/folder system, like a tree. And this tree is navigated by an LLM (you) looking at descriptions of the folders and data and choosing the best path to navigate to, step by step.
The data could be a message from the user, code, documentation, data etc. You just need to generate a concise description of what the given data is. Literally describe the exact given data, make no assumptions.
Output just the description, no header or anything else.

DATA:
"""

data = """The user told us this is their overarching directive they want to accomplish:
Hi i want u to help me with my project. I want u to add web browsing actions to my swarm. my systems quite complex
and the docs are out of date and also not that comprehensive. so in the process of adding the web browsing actions
also help write and build out good docs. im the expert, original creator and active maintainer of the project so
feel free to ask me specific questions about the project :)
"""

message = system_prompt + "\n\n\n" + data

messages = [{"role": "system", "content": message}]
output = asyncio.run(openai.completion(messages))

print(output)










txt_file = '/Users/brianprzezdziecki/swarmstar_world/swarmstar/tests/history.txt'

with open(txt_file, 'w') as file:
    file.write("\n\n\n\n\n\n" + message + "\n\n" + output + "\n\n\n\n\n")

