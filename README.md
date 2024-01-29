# Warning
**UPDATE. Documentation is not just shit. its not up to date.**
**Not available yet. Still undergoing development before it's ready for use.**
**Documentation is also still shit. i dont expect anyone to understand this yet.**
**aiming to have a proper package, web app interface and documentation by February 10 2024**


**reminder to myself. make it clear in the docs when i do them to put the swarm space in gitignore because it holds all your private keys**

# Autonomous General Agent Swarm
this system is designed to be a general purpose agent swarm. you give it any arbitrary goal, simply as a string and it will do its best to fullfill it. it will use any and all resources available to it to do so, including creating new tools autonomously. it will communicate with you throughout the process, asking for help and requirement specifications when it needs it. 

if ur a coder there will be more configuration youll be able to do. the package will be compatible with serverless and any provider, or you can run it on your own hardware. 

An agent swarm is a collection of agents working together to achieve a common goal. An agent is an autonomous entity that can perceive its environment and take actions to achieve its goals. 

Also documenting on youtube @ [AI Agent Swarm Playlist](https://youtube.com/playlist?list=PLO8gVow6df_Rh7DEJ10_WAdnkGnIRCh-K&si=eYdyBu7NShKckilS)


# Guiding Principles
Aim to maximize the following:
    1. Simple
    2. General
    3. Autonomous 

Strategically build to take advantage of SOTA models, incorporating new modalities and emergent capabilities

# Usage
Not available yet. Still undergoing development before it's ready for use.

# Architecture
## Design Principles
    1. Heavy bias torwards action 
    2. Communication should primarily be focused around requirements and directives
    3. Aim for self sufficiency and autonomy

## Internal Swarm Communication

## Action and Memory Space
Fundamentally there are two parts of the swarm - actions and memory. 

These spaces, the action and memory space, are navigated by "router" agents. Router agents decide where to go to fullfill a directive. Action routers decide what action to take, and memory routers help find the information to answer or assist you. 

The action and memory space are organized as trees for scalability, ease of navigation and just because it's intuitive to store things as a tree. It's like a file structure, or a book with chapters, sections etc. Trees are scalable because retrieval within a tree is O(log n) time complexity. Additionally we need to utilize trees for the routers since we can't flood the router with every possible choice at once, but only a limited amount at a time.  

### Action Space


### Memory Space

