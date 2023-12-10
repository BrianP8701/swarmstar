# Tool Building Experiment

## Usage
Set OPENAI_API_KEY in .env file in root.
Create swarm object and call the start function with any arbitrary goal. Example run in test.py

## Architecture
These are the main, most important files:

config/
    agents.json
    functions.json
swarm/
    agent.py
    swarm.py
    task_handler.py

agents.json essentially contains premade agent definitions for the swarm. In my project agents simply contain one tool and a description. 
and then obv agent.py is just the agent object with a chat function to use the tool
functions.json just contains code written as strings. this is because we want the
