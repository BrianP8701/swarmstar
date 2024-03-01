# Swarm Space Configuration
The SwarmConfig object allows you to configure the swarm package to work on your platform.

It might look like a lot, but trust me this step is really simple (I hope it's simple lmao please contact me if you have trouble). Don't read too much into the SwarmConfig model below, we'll break it down step by step.

<span class="pathname">swarmstar/swarm/types/swarm_config.py</span>
``` py
class SwarmConfig(BaseModel):
    root_path: str
    openai_key: str
    platform: Literal["mac", "azure"]
    user_id: Optional[str] = None
    swarm_id: Optional[str] = None
    kv_operations_path: Optional[str] = None
    folder_operations_path: Optional[str] = None
    file_operations_path: Optional[str] = None
    # azure keys, mongodb keys etc as needed...
```

Let's go through this step by step. The openai_key is self explanatory so we'll skip that one. Platform allows you to select what your running on. Now might be a good time to explain WHY I need this information from you.

## What is swarmstar space?
The swarm interacts with data a lot. It needs a place to save it's code, history, state, dynamically generated actions, memories and more. You can think of this as the "space" in which the swarm exists and operates. 

