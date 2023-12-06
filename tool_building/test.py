import json
from swarm.agent import Agent
import asyncio
from swarm.swarm import Swarm



swarm = Swarm()
print(asyncio.run(swarm.start('Create a class called GithubWrapper that has all the necessary functions to interact with and modify a Github repository.')))