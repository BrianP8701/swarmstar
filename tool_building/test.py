import json
from swarm.agent import Agent
import asyncio

with open('tool_building/swarm/agent_config.json') as f:
    agent_config = json.load(f)
agent = Agent(agent_config['head_agent']['instructions'], agent_config['head_agent']['tools'])

print(asyncio.run(agent.chat('Create a new revolutionary CRM for real estate agents that takes advantage of chatgpt')))