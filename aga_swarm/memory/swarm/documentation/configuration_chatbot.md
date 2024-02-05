# Non technical overview
## What is the swarm?
The swarm's aim is to automate as much as possible. 

Today, coders often gather relevant context and explain requirements to ChatGPT, which will try to help you make a solution or write code. If the solution is correct the coder will put it to use.

The swarm has a singular entrypoint for the user: An explanation of the users goal and all relevant context the user thinks to provide. The swarm will then autonomously pursue this goal, breaking it down, writing and saving code to the right place, autonomously navigating its memory, and importantly, it will be able to ask you questions if it needs more context. This is not a full automation of the software engineer. The engineer remains to make high level system, product and design choices. As foundational models improve and become more capable, the engineer may work in a more abstract space of ideas, spending more time directing his swarm.

## Swarm Implementation
The fundamental unit of the swarm is a node. Each node takes a directive (string) and performs a singular action. 

You instantiate the swarm by spawning a node with a singular directive and as much context you believe necessary. The root node will spawn specialized nodes that will organize and store the context in the swarms memory. The root node will spawn a manager node that will break down the directive into a series of sub-directives to be performed immediately in parralel. The manager node will spawn an action router node for each sub-directive. The action router will search the action space for the best action to perform given the directive. Thus, each action router will spawn a node with an assigned action, which might be to further break down the goal, ask the user questions etc.

The entirety of the swarm follows a tree structure growing from the root node. As the tree grows and directives get broken down into small enough components, eventually a node will be able to accomplish and complete its directive. It will then terminate, and pass a report to it's parent. The parent, if all its children are dead will also proceed to terminate. Whenever a manager node tries to terminate, it will first review all the reports of its children and make sure that the directive has been completed. If the directive has not been completed, the manager will spawn a new manager to create the next set of subdirectives and the process will continue. When the root node has terminated the intial directive has been completed.

## Action Space
Every node in the swarm corresponds to a singular action. Every action outputs and accepts a directive. Examples of actions are: decompose_directive, write_python, review_reports, determine_unknown_requirements etc. The action space is navigated using the metadata of each action, which is organized into a tree/file like structure. 

## Swarm Util Space
This space consists of specific util functions that are used by the swarm. When the swarm attempts to autonomously create a new action it might need to make use of utils from this space.

## Memory Space
The memory space contains the work of the swarm and other relevant information, like user provided context, documentation and rules the swarm uses to understand itself and more. This space is autonomously managed. Nodes in the swarm will often search this space for context to understand their directives, which if they can't find they will ask the user for.
