# What is a swarm operation?
Swarm operations classify the types of operations nodes can perform. There are 4 broad classes of operations, which each have distinct types.

<span class="pathname">swarmstar/swarm/types/swarm.py</span>
``` pyclass SwarmOperation(BaseModel):
    operation_type: Literal['spawn', 'terminate', 'node_failure', 'blocking']
    node_id: str
```