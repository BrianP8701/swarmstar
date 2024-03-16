from typing import List, Union
import inspect

from swarmstar.models import (
    SwarmConfig,
    SwarmOperation,
    SpawnOperation,
    NodeEmbryo,
    SwarmState,
    SwarmHistory
)
from swarmstar.utils.swarm_operations import (
    blocking,
    failure,
    spawn,
    terminate,
    execute_action
)
from swarmstar.utils.data import MongoDBWrapper
from swarmstar.utils.context import root_path_var

db = MongoDBWrapper()

class Swarmstar:
    def __init__(self, swarm_config: SwarmConfig):
        self.swarm_config = swarm_config
        self.swarm_id = swarm_config.id
        self._set_context()

    def spawn_root(self, goal: str) -> SpawnOperation:
        """
        Create the first spawn operation for the swarm.
        """
        db.insert("swarm_history", self.swarm_id, {"data": []})
        db.insert("swarm_state", self.swarm_id, {"data": []})
        SwarmConfig.add_swarm_config(self.swarm_config)
        root_spawn_operation = SpawnOperation(
            node_embryo=NodeEmbryo(
                action_id='swarmstar/actions/reasoning/decompose_directive',
                message=goal
            )
        )
        
        SwarmOperation.insert_swarm_operation(root_spawn_operation)
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
                operation_func = operation_mapping[swarm_operation.operation_type]
                
                if swarm_operation.operation_type == "spawn":
                    output = operation_func(self.swarm_id, swarm_operation)
                elif inspect.iscoroutinefunction(operation_func):
                    output = await operation_func(swarm_operation)
                else:
                    output = operation_func(swarm_operation)        
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
            SwarmOperation.insert_swarm_operation(operation)

        # Add executed operation to swarm history
        SwarmHistory.add_swarm_operation_id_to_swarm_history(self.swarm_config.id, swarm_operation.id)

        return output

    @staticmethod
    def delete_swarmstar_space(swarm_id: str) -> None:
        swarm_node_ids = SwarmState.get_swarm_state(swarm_id)
        for swarm_node_id in swarm_node_ids:
            db.delete("swarm_nodes", swarm_node_id)
        
        swarm_operation_ids = SwarmHistory.get_swarm_history(swarm_id)
        for swarm_operation_id in swarm_operation_ids:
            db.delete("swarm_operations", swarm_operation_id)
        
        db.delete("config", swarm_id)
        db.delete("swarm_state", swarm_id)
        db.delete("swarm_history", swarm_id)
        
        admin = db.get("admin", "swarms")
        admin["data"].remove(swarm_id)
        db.set("admin", "swarms", admin)

    def _set_context(self):
        root_path_var.set(self.swarm_config.root_path)
