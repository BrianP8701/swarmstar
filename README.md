# Agent_Swarm_Experiments
Making experiments locally to contribute to AGI

## Usage
First, configure the .env file. Each subfolder contains an idea or experiment (RAG/agent swarm related). Each experiment contains a plan.md file for my personal use (likely not of any use to you), and a docs.md which you should read. The docs.md will contain usage instructions, architecture details etc.

In the rest of this file I will describe the motivation and takeaways of each experiment.

## Experiments

In theory - or my imagination at least - there ought to be an inflection point where the swarm becomes self sufficient. 

The swarm needs to be self aware that it is a swarm. The top agents need to know about the system they operate in. They need sufficient context. Lower agents who gain more and more specific tasks will need less context.

### Tool Building Experiment
Goal: Have agents autonomously make new python functions that can be used by the swarm