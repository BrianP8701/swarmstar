# Test run the swarm


import json
from swarm.agent import Agent
import asyncio
from swarm.swarm import Swarm
from task import Task

# with open('tool_building/config/agents.json') as f:
#     agent_schemas = json.load(f)
# head_agent = Agent(agent_schemas['head_agent']['instructions'], agent_schemas['head_agent']['tools'], agent_schemas['head_agent']['tools'][0]['function']['name'])
# what = head_agent.chat('Create a class called GithubWrapper that has all the necessary functions to interact with and modify a Github repository.')
# print(what)



swarm = Swarm('tool_building/past_runs/test_write_python_2.json')
goal = 'Create a class called GithubWrapper that has all the necessary functions to interact with and modify a Github repository.'
context = '3'
asyncio.run(swarm.start('Create a class called GithubWrapper that has all the necessary functions to interact with and modify a Github repository.'))

# test_data = {'subtasks': ['Define the scope and functionalities required for the GithubWrapper class.', 'Research the GitHub API documentation to understand the endpoints needed for the functionalities.', 'Set up the authentication process to securely interact with the GitHub API.'], 'context': 'The goal is to create a GithubWrapper class that can interact with and modify a Github repository. To achieve this, we need to first define what functionalities the class should have, such as creating issues, pulling requests, managing files, etc. Then, we need to understand how to use the GitHub API to implement these functionalities. Finally, we need to ensure that the class can authenticate with GitHub to perform actions on behalf of a user.', 'is_parallel': True}

# test_write_python_data = {'goal': "Context to understand the task: The goal is to create a class called GithubWrapper that will encapsulate the functionalities needed to interact with and modify a GitHub repository. This will involve understanding the GitHub API, designing the class, and implementing the methods.\n\n\n The task: Set up the authentication process to securely interact with the GitHub API."}
# task = Task('write_python', test_write_python_data)

# print(asyncio.run(swarm.test(task)))

