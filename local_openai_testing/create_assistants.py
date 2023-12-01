from openai_config import get_openai_client
import json
import time

client = get_openai_client()

# Create assistant
# Get json file as dict:
with open('/Users/brianprzezdziecki/Code/Agent_Swarm_Experiments/tool_building/swarm/tool_config.json') as f:
    tool_dict = json.load(f)
    
tools = tool_dict['head_agent_tools']['items']
name = 'Head_Agent'
instructions = 'You are in charge of a swarm of agents. Given the goal, current progress and context command the swarm to pursue the goal.'

# assistant = client.beta.assistants.create(instructions=instructions,name=name,tools=tools,model='gpt-4-1106-preview')


# run = client.beta.threads.create_and_run(
#   assistant_id="asst_1cfAUDgvFu8Jr8QYqU5nnF9R",
#   thread={
#     "messages": [
#       {"role": "user", "content": "Create a new revolutionary CRM for real estate agents that takes advantage of chatgpt"}
#     ]
#   }
# )
# print(run)
# time.sleep(10)
# print(run)

# my_thread = client.beta.threads.retrieve("thread_BE0MD6WtPWyvdVOQ4viomobu")
# print(my_thread)

# thread_messages = client.beta.threads.messages.list("thread_BE0MD6WtPWyvdVOQ4viomobu")
# print(thread_messages.data)

# Retrieve run by id run_bJ7jha8Sfa5FavX6ojaSMfm1
run = client.beta.threads.runs.retrieve(
  thread_id="thread_BE0MD6WtPWyvdVOQ4viomobu",
  run_id="run_bJ7jha8Sfa5FavX6ojaSMfm1"
)
print(run)