from typing import List, Union
import inspect

from swarmstar.models import (
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
from swarmstar.context import swarm_id_var

db = MongoDBWrapper()

class Swarmstar:
    def __init__(self, swarm_id: str):
        self._set_context(swarm_id)

    def spawn(self, goal: str) -> SpawnOperation:
        """
        Spawn a new swarm with the given goal.
            - Creates initial swarmstar space
            - Create and return the root spawn operation
        
        :param goal: The goal of the new swarm
        :return: The root spawn operation for the new swarm
        """
        self._create_swarmstar_space(swarm_id_var.get())

        root_spawn_operation = SpawnOperation(
            node_embryo=NodeEmbryo(
                action_id='specific/managerial/conduct_introductory_interview',
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
        SwarmHistory.append(swarm_id_var.get(), swarm_operation.id)

        return output

    def _create_swarmstar_space(self, swarm_id: str) -> None:
        memory_space = MemoryMetadata.clone(swarm_id)
        # TODO - Clone action and util metadata as well
        swarmstar_space = {
            "swarm_state": [],
            "swarm_history": [],
            "memory_space": memory_space,
            "action_space": [],
            "util_space": []
        }
        db.insert("admin", swarm_id, swarmstar_space)
        db.append_to_list("admin", "swarm_ids", "data", swarm_id)

    @staticmethod
    def delete_swarmstar_space(swarm_id: str) -> None:
        swarm_node_ids = SwarmState.get(swarm_id)
        for swarm_node_id in swarm_node_ids:
            db.delete("swarm_nodes", swarm_node_id)
        
        swarm_operation_ids = SwarmHistory.get(swarm_id)
        for swarm_operation_id in swarm_operation_ids:
            db.delete("swarm_operations", swarm_operation_id)

        admin = db.get_by_key("admin", "swarm_ids", "data")
        admin.remove(swarm_id)
        db.update("admin", "swarm_ids", {"data": admin})
        db.delete("admin", swarm_id)

        MemoryMetadata.delete_external_memory_metadata_tree(swarm_id)



    def _set_context(self, swarm_id: str) -> None:
        swarm_id_var.set(swarm_id)
