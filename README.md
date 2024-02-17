# Warning
**Not available yet. Still undergoing development before it's ready for use.**

**aiming to have a proper package, web app interface and documentation by February 10 2024**

**failed to meet deadline. package is essentially ready, just need to add some actions which is easy. frontend is taking longer than expected. Lets say done by February 15 2024. I swear on it**

**Im such a fucking failure. im sorry boys the frontend took longer than i expected its my first time. i promise im nearly done with the interface and ill come back to this package**

I think if ur interested in the project a great place to look to understand whats going on is in the types folder. swarm_star/swarm/types

**reminder to myself. make it clear in the docs when i do them to put the swarm space in gitignore because it holds all your private keys**

# Swarm Star
# Non Technical Overview
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

Also documenting on youtube @ [AI Agent Swarm Playlist](https://youtube.com/playlist?list=PLO8gVow6df_Rh7DEJ10_WAdnkGnIRCh-K&si=eYdyBu7NShKckilS)


# Guiding Principles
Aim to maximize the following:
1. Simple
2. General
3. Autonomous 
4. Scalable

Strategically build to take advantage of SOTA models, incorporating new modalities and emergent capabilities.

# Usage
Not available yet. Still undergoing development before it's ready for use.

# Architecture
## Design Principles
1. Heavy bias torwards action.
2. Communication should primarily be focused around requirements and directives.
3. Aim for self sufficiency and autonomy. Constantly automate. We will automate and eat the world. 
4. The swarm should be able to operate in a completely decentralized manner. 

## Internal Swarm Communication

## Action and Memory Space
Fundamentally there are two parts of the swarm - actions and memory. 

These spaces, the action and memory space, are navigated by "router" agents. Router agents decide where to go to fullfill a directive. Action routers decide what action to take, and memory routers help find the information to answer or assist you. 

The action and memory space are organized as trees for scalability, ease of navigation and just because it's intuitive to store things as a tree. It's like a file structure, or a book with chapters, sections etc. Trees are scalable because retrieval within a tree is O(log n) time complexity. Additionally we need to utilize trees for the routers since we can't flood the router with every possible choice at once, but only a limited amount at a time.  

### Action Space
The action space is for searching for the right action to take

### Memory Space
The memory space is for searching for the right memory/information to use.

### Swarm Util Space
The util space is for searching for the right util to use. 





categories in kv_store
kv_store is stored at {root_path}/swarm_default_kv_store.db on local, or cosmosdb on azure

on local keys follow: {category}_{key}
action_space_{action_id} = ActionMetadata
memory_space_{memory_id} = MemoryMetadata
util_space_{util_id} = SwarmUtilMetadata
swarm_state_{node_id} = SwarmNode
swarm_history_current_frame = int
swarm_history_{frame} = SwarmEvent



on cosmosdb keys follow: {user_id}_{swarm_id}_{category}_{key}
same as above but with user_id and swarm_id in front

