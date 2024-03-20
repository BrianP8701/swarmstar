from typing import List, Union
import inspect

from swarmstar.models import (
    SwarmOperation,
    SpawnOperation,
    NodeEmbryo,
    MemoryMetadata,
    SwarmstarSpace
)
from swarmstar.swarm_operations import (
    blocking,
    spawn,
    terminate,
    execute_action
)
from swarmstar.database import MongoDBWrapper
from swarmstar.context import swarm_id_var

db = MongoDBWrapper()

class Swarmstar:
    def __init__(self, swarm_id: str):
        swarm_id_var.set(swarm_id)

    def spawn(self, goal: str) -> SpawnOperation:
        """
        Spawn a new swarm with the given goal.
            - Creates initial swarmstar space
            - Create and return the root spawn operation
        
        :param goal: The goal of the new swarm
        :return: The root spawn operation for the new swarm
        """
        SwarmstarSpace.instantiate_swarmstar_space(swarm_id_var.get())

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
            SwarmOperation.save(operation)

        return output        
