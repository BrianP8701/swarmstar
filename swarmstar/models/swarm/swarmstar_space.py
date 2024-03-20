"""
Swarmstar space describes the entirety of what makes up a swarm: 
    - Swarm nodes
    - Swarm operations
    - Memory tree
    - Action tree
The SwarmstarSpace class is a model that provides a high level interface to instantiate,
clone and delete swarmstar spaces.

Every object in the swarmstar space follows a common format for their ids
    {swarm_id}_{x}{y}
where x is a marker for the type of object:
    - n: node
    - o: operation
    - m: memory
    - a: action
and y is simply the number, taken in order of creation

This id convention makes it easier to manage everything
"""
from pydantic import BaseModel
from typing import List

from swarmstar.models import (
    MemoryMetadataTree,
    ActionMetadataTree,
    SwarmTree,
    SwarmOperation
)
from swarmstar.utils.database import MongoDBWrapper

db = MongoDBWrapper()

class SwarmstarSpace(BaseModel):
    node_count: int # The number of nodes in the swarmstar space
    operation_count: int # The number of operations in the swarmstar space
    memory_count: int # The number of external memories in the swarmstar space
    action_count: int # The number of external actions in the swarmstar space
    queued_operation_ids: List[str] = [] # Ids of operations that have not yet been executed

    @staticmethod
    def get(swarm_id: str):
        return db.get("admin", swarm_id)

    @staticmethod
    def instantiate_swarmstar_space(swarm_id: str):
        if db.exists("admin", swarm_id):
            raise ValueError(f"Swarmstar space with id {swarm_id} already exists")

        swarmstar_space = {
            "node_count": 0,
            "operation_count": 0,
            "memory_count": 0,
            "action_count": 0,
        }

        MemoryMetadataTree.instantiate(swarm_id)
        ActionMetadataTree.instantiate(swarm_id)

        db.insert("admin", swarm_id, swarmstar_space)

    @staticmethod
    def clone_swarmstar_space(old_swarm_id: str, new_swarm_id: str):
        if not db.exists("admin", old_swarm_id):
            raise ValueError(f"Swarmstar space with id {old_swarm_id} does not exist")
        if db.exists("admin", new_swarm_id):
            raise ValueError(f"Swarmstar space with id {new_swarm_id} already exists")

        SwarmTree.clone(old_swarm_id, new_swarm_id)
        ActionMetadataTree.clone(old_swarm_id, new_swarm_id)
        MemoryMetadataTree.clone(old_swarm_id, new_swarm_id)

        old_swarmstar_space = SwarmstarSpace.get(old_swarm_id)
        for i in range(old_swarmstar_space.operation_count):
            SwarmOperation.clone(f"{old_swarm_id}_o{i}", new_swarm_id)
        old_swarmstar_space.queued_operation_ids = [f"{new_swarm_id}_o{operation_id.split('_o')[1]}" \
            for operation_id in old_swarmstar_space.queued_operation_ids]
        
        db.insert("admin", new_swarm_id, old_swarmstar_space)

    @staticmethod
    def delete_swarmstar_space(swarm_id: str):
        if not db.exists("admin", swarm_id):
            raise ValueError(f"Swarmstar space with id {swarm_id} does not exist")

        SwarmTree.delete(swarm_id)
        ActionMetadataTree.delete(swarm_id)
        MemoryMetadataTree.delete(swarm_id)
        
        old_swarmstar_space = SwarmstarSpace.get(swarm_id)
        for i in range(old_swarmstar_space.operation_count):
            SwarmOperation.delete(f"{swarm_id}_o{i}")

        db.delete("admin", swarm_id)
