# Termination Operations
## What is a termination operation?
Nodes terminate upon completion of their task. Crucially a node cannot terminate until all of it's children have terminated. 

<span class="pathname">swarmstar/swarm/types/swarm.py</span>
``` py
class TerminationOperation(SwarmOperation):
    operation_type: Literal['terminate']
    node_id: str
```

Each node has a termination policy assigned to it. Some examples of termination policies:

- 'Simple termination' refers to when a node terminates and creates a Termination Operation for it's parent.
- 'Parralel review termination' is designated to the decompose directive node. This node decomposes a directive into immedate parralel subdirectives, for which it spawned child nodes for. This node must ensure all children are terminated before it terminates. In addition it must perform a review process to determine if the goal has been accomplished, or if it needs to create a new set of subdirectives and nodes. If all children have been terminated and there has been a successful review it will consolidate the reports of it's children and terminate.
- 'Clone with reports' is for nodes that had questions about their directives. These nodes spawned a node to get answers from other nodes or the user. When this branch completes, and the termination propagates back up to it, this node will clone itself with the answers from that child node's reports.

These are just a few example of termination policies in the swarm. This allows us to facilitate some communication amongst nodes and direct their lifecycle.