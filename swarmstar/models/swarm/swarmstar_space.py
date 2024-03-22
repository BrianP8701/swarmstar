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

from swarmstar.models.metadata.memory_metadata_tree import MemoryMetadataTree
from swarmstar.models.metadata.action_metadata_tree import ActionMetadataTree
from swarmstar.models.swarm.swarm_tree import SwarmTree
from swarmstar.models.swarm.swarm_operations import SwarmOperation

from swarmstar.utils.database import MongoDBWrapper

db = MongoDBWrapper()

class SwarmstarSpace(BaseModel):
    node_count: int # The number of nodes in the swarmstar space
    operation_count: int # The number of operations in the swarmstar space
    memory_count: int # The number of external memories in the swarmstar space
    action_count: int # The number of external actions in the swarmstar space
    queued_operation_ids: List[str] = [] # Ids of operations that have not yet been executed

    @staticmethod
    def read(swarm_id: str) -> 'SwarmstarSpace':
        return SwarmstarSpace(**db.read("admin", swarm_id))

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

        db.create("admin", swarm_id, swarmstar_space)

    @staticmethod
    def clone_swarmstar_space(old_swarm_id: str, new_swarm_id: str):
        if not db.exists("admin", old_swarm_id):
            raise ValueError(f"Swarmstar space with id {old_swarm_id} does not exist")
        if db.exists("admin", new_swarm_id):
            raise ValueError(f"Swarmstar space with id {new_swarm_id} already exists")

        old_swarmstar_space = SwarmstarSpace.read(old_swarm_id)

        if old_swarmstar_space.node_count > 0: SwarmTree.clone(old_swarm_id, new_swarm_id)
        if old_swarmstar_space.action_count > 0: ActionMetadataTree.clone(old_swarm_id, new_swarm_id)
        if old_swarmstar_space.memory_count > 0: MemoryMetadataTree.clone(old_swarm_id, new_swarm_id)

        batch_copy_payload = [[], []] # [old_ids, new_ids]
        batch_update_payload = {} #{old_operation_id: {updated_fields}}
        for i in range(old_swarmstar_space.operation_count):
            old_op_id = f"{old_swarm_id}_o{i}"
            operation = SwarmOperation.read(old_op_id)
            updated_fields = operation.get_field_updates_on_copy(new_swarm_id)
            batch_copy_payload[0].append(old_op_id)
            batch_copy_payload[1].append(f"{new_swarm_id}_o{i}")
            batch_update_payload[f"{new_swarm_id}_o{i}"] = updated_fields
        db.batch_copy("swarm_operations", batch_copy_payload[0], batch_copy_payload[1])
        db.batch_update("swarm_operations", batch_update_payload)

        old_swarmstar_space.queued_operation_ids = [f"{new_swarm_id}_o{operation_id.split('_o')[1]}" \
            for operation_id in old_swarmstar_space.queued_operation_ids]
        db.create("admin", new_swarm_id, old_swarmstar_space)

    @staticmethod
    def delete_swarmstar_space(swarm_id: str):
        if not db.exists("admin", swarm_id):
            raise ValueError(f"Swarmstar space with id {swarm_id} does not exist")

        swarmstar_space = SwarmstarSpace.read(swarm_id)
        db.delete("admin", swarm_id)
        
        if swarmstar_space.node_count > 0: SwarmTree.delete(swarm_id)
        if swarmstar_space.action_count > 0: ActionMetadataTree.delete(swarm_id)
        if swarmstar_space.memory_count > 0: MemoryMetadataTree.delete(swarm_id)
        
        for i in range(swarmstar_space.operation_count):
            SwarmOperation.delete(f"{swarm_id}_o{i}")
