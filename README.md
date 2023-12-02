# Agent_Swarm_Experiments
Making experiments locally to contribute to AGI

## Usage
Create a .env file at the project root and set your OPENAI_API_KEY's value in there. Each subfolder contains an idea or experiment (RAG/agent swarm related). Each experiment contains a plan.md file for my personal use, and a docs.md file for you.

In the rest of this file I will describe the motivation and takeaways of each experiment.

## Experiments

In theory - or my imagination at least - there ought to be an inflection point where the swarm becomes self sufficient. 

The swarm needs to be self aware that it is a swarm. The top agents need to know about the system they operate in. They need sufficient context. Lower agents who gain more and more specific tasks will need less context.

### Tool Building Experiment
Goal: Have agents autonomously make new python functions that can be used by the swarm