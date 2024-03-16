import asyncio

from swarmstar import Swarmstar
from swarmstar.models import SwarmConfig

from swarmstar.utils.ai.openai import OpenAI

openai = OpenAI()

completion = asyncio.run(openai.completion([{"role": "system", "content": "say hi"}]))

print(completion)
print(type(completion))