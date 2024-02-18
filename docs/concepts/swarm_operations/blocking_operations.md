# Blocking Operations
## What are blocking operations?
This operation exists for technical reasons. Blocking operations are things that block the execution of the action, like making a request to openai, waiting for user input or performing any CPU or I/O bound task. 

<span class="pathname">swarmstar/swarm/types/swarm.py</span>
``` py
class BlockingOperation(SwarmOperation):
    operation_type: Literal['blocking']
    node_id: str
    blocking_type: str  
    args: Dict[str, Any] = {}
    context: Dict[str, Any] = {}
    next_function_to_call: str 
```

The blocking_type attribute indicates how to handle this blocking operation. The args section holds the arguments to pass to execute this blocking operation. Context holds data that needs to be passed back when we resume execution in the action upon completion of the blocking operation. Given the action_id, we simply call the next_function_to_call in the action with the context and blocking operation output.