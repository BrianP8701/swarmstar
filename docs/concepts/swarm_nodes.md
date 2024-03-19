# Swarm Nodes
The swarm node is the fundamental unit of the swarm. You can think of each node as an **agent** or **action**.

<span class="pathname">swarmstar/swarm/types/swarm.py</span>
``` py
class SwarmNode(BaseModel):
    node_id: str
    parent_id: str = None
    children_ids: List[str]
    action_id: str
    message: str
    report: str = None
    alive: bool
    termination_policy: Literal[
        'simple',
        'confirm_directive_completion', 
        'clone_with_questions_answered'
    ] 
```
Nodes are classified by their action_id (defined in [Action Space](action_space.md)) which is assigned at spawn. The node executes the predefined action given the message. The message comes from the parent node, or in the case of the root node the user. The message contains the directive and context. 

Nodes are stored in [Swarm State](swarm_state.md).

When nodes are spawned they execute their designated action. Execution of the action will produce [Swarm Operations](swarm_operations/index.md).

For example, nodes may spawn and designate actions to children nodes. This logic is rigid and predefined in each action. Nodes may terminate when they complete their tasks according to their [termination policy](swarm_operations/termination_operations.md). No node can terminate until all children have terminated. 

## Node Communication
    - Directives
    - Requirements and intent
    - Reports

When spawning a child the node passes a directive making their requirements and intent clear.

When nodes terminate they create a report concluding the success or failure of their operation.

## Portal Nodes
In a metadata tree, we store a default metadata tree in the internal sqlite database to be reused in every swarm instance. However, we want to allow every swarm to be able to add onto the memory and action space as needed. This means the internal nodes need to somehow allow a connection to external nodes, by storing in their children_ids an external node.

We could simply copy the entire metadata tree for each node but this would be wasteful as the internal metadata tree is meant to be immutable. 