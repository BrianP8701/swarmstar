from typing import List, Union
import inspect

from swarmstar.models import (
    SwarmConfig,
    SwarmOperation,
    SpawnOperation,
    NodeEmbryo,
    SwarmState,
    SwarmHistory,
    MemoryMetadata,
)
from swarmstar.utils.swarm_operations import (
    blocking,
    failure,
    spawn,
    terminate,
    execute_action
)
from swarmstar.utils.data import MongoDBWrapper
from swarmstar.utils.context import swarm_id_var

db = MongoDBWrapper()

class Swarmstar:
    def __init__(self, swarm_config: SwarmConfig):
        self.swarm_config = swarm_config
        self.swarm_id = swarm_config.id
        self._set_context()

    def spawn(self, goal: str) -> SpawnOperation:
        """
        Spawn a new swarm with the given goal.
            - Creates initial swarmstar space
            - Create and return the root spawn operation
        
        :param goal: The goal of the new swarm
        :return: The root spawn operation for the new swarm
        """
        self._create_swarmstar_space(self.swarm_id)

        root_spawn_operation = SpawnOperation(
            node_embryo=NodeEmbryo(
                action_id='swarmstar/actions/reasoning/decompose_directive',
                message=goal
            )
        )

        SwarmOperation.save(root_spawn_operation)
        return root_spawn_operation

    async def execute(self, swarm_operation: SwarmOperation) -> Union[List[SwarmOperation], None]:
        """
        This function is the main entry point for the swarmstar library. It takes in a swarm configuration and a swarm operation
        and returns a list of swarm operations that should be executed next.
        """
        
        operation_mapping = {
            "spawn": spawn,
            "blocking": blocking,
            "terminate": terminate,
            "node_failure": failure,
            "action": execute_action,
        }

        if swarm_operation.operation_type in operation_mapping:
            try:
                operation_handler = operation_mapping[swarm_operation.operation_type]
                
                if inspect.iscoroutinefunction(operation_handler):
                    output = await operation_handler(swarm_operation)
                else:
                    output = operation_handler(swarm_operation)   
     
            except Exception as e:
                print(f"Error in execute_swarmstar_operation: {e}")
                raise e
        else:
            raise ValueError(
                f"Unknown swarm operation type: {swarm_operation.operation_type}"
            )

        if output is None:
            return None
        elif isinstance(output, SwarmOperation):
            output = [output]
        elif not isinstance(output, list):
            raise ValueError(f"Unexpected return type from operation_func: {type(output)}")

        for operation in output:
            # Insert new operations into the swarm operations collection
            SwarmOperation.save(operation)

        # Add executed operation to swarm history
        SwarmHistory.append(self.swarm_config.id, swarm_operation.id)

        return output

    def _create_swarmstar_space(self, swarm_id: str) -> None:
        memory_space = MemoryMetadata.clone(swarm_id)
        # TODO - Add action space and util space
        swarmstar_space = {
            "swarm_state": [],
            "swarm_history": [],
            "memory_space": memory_space,
            "action_space": [],
            "util_space": [],
            "config": self.swarm_config.model_dump()
        }
        db.insert("admin", swarm_id, swarmstar_space)

    @staticmethod
    def delete_swarmstar_space(swarm_id: str) -> None:
        swarm_node_ids = SwarmState.get(swarm_id)
        for swarm_node_id in swarm_node_ids:
            db.delete("swarm_nodes", swarm_node_id)
        
        swarm_operation_ids = SwarmHistory.get(swarm_id)
        for swarm_operation_id in swarm_operation_ids:
            db.delete("swarm_operations", swarm_operation_id)
        
        db.delete("config", swarm_id)
        db.delete("swarm_state", swarm_id)
        db.delete("swarm_history", swarm_id)
        
        admin = db.get("admin", "swarms")
        admin["data"].remove(swarm_id)
        db.replace("admin", "swarms", {"data": admin["data"]})

    def _set_context(self):
        print(f"Setting context to {self.swarm_config.id}")
        swarm_id_var.set(self.swarm_config.id)
