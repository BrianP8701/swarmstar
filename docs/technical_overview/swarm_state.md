

## When to update swarm state

We update swarm state whenever we change or add a new node. This includes when we:
    - spawn a node
    - add a report to a node
    - change a node's termination policy
    - terminate a node
Ideally we would update a node after every swarm operation. 