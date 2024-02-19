# Spawn Operation
The spawn operation will spawn and begin execution of a node. It creates a swarm object from the NodeEmbryo and adds it to the [Swarm State](../swarm_state.md).

<span class="pathname">swarmstar/swarm/types/swarm.py</span>
``` py
class NodeEmbryo(BaseModel):
    action_id: str
    message: str

class SpawnOperation(SwarmOperation):
    operation_type: Literal['spawn']
    node_embryo: NodeEmbryo
    termination_policy_change: Literal[
        'simple',
        'parallel_review', 
        'clone_with_reports'
    ] = None
    node_id: str
```
When you first pass your goal to the swarm you'll create a Spawn Operation that will decompose your goal. This is the decompose directive action. Other than that, Spawn Operations will always be created by Swarm Nodes. 

The action_id refers to the action to perform in the [Action Space](../action_space.md). The node_id in the Spawn Operation object refers to the parent node that spawned this node. 