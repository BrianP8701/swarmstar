# onno
Building AGI and beyond. Documenting my journey on YouTube @ [AI Agent Swarm Playlist](https://youtube.com/playlist?list=PLO8gVow6df_Rh7DEJ10_WAdnkGnIRCh-K&si=eYdyBu7NShKckilS)

# Warning
**Not available yet. Still undergoing development before it's ready for use.**
**Documentation is also still shit. i dont expect anyone to understand this yet.**

# Guiding Principles
    1. Make everything as simple as possible
    2. Make swarm universally applicable/infinitely scalable to any goal
    3. Strategically build to take advantage of SOTA models, their emergent capabilities and new modalities 
    4. Make the swarm self sufficient and capable of recursive self improvement

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

