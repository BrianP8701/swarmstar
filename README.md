# Agent_Swarm_Experiments
Making experiments locally to contribute to AGI. Documenting my journey on YouTube @ [AI Agent Swarm Playlist](https://youtube.com/playlist?list=PLO8gVow6df_Rh7DEJ10_WAdnkGnIRCh-K&si=eYdyBu7NShKckilS)

# Principles
    1. Make everything as simple as possible
    2. Make swarm universally applicable/infinitely scalable to any goal
    3. Strategically build to take advantage of SOTA models, their emergent capabilities and new modalities 
    4. Make the swarm self sufficient and capable of recursive self improvement

# Usage
1. Create an instance of the swarm class
2. Call load_goal() to give the swarm a goal
3. Call run()

# Architecture
Fundamentally there are two parts of the swarm - actions and memory. 
These spaces, the action and memory space, are navigated by "router" agents. Router agents have a task, query or request sent to them and decide where to go to fullfill it. Action routers decide what action to take, and memory routers help find the information to answer or assist you. 
The action and memory space are organized as trees for scalability, ease of navigation and just because it's intuitive to store things as a tree. It's like a file structure, or a book with chapters, sections etc. Trees are scalable because retrieval within a tree is O(log n) time complexity. Additionally we need to utilize trees for the routers since we can't flood the router with every possible choice at once, but only a limited amount at a time. 