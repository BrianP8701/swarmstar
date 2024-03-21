"""
If your using swarmstar, this is the only file you need to import and interact with.

First of all, make sure to have your .env file set up. You can use the .env.example file as a template.
Then, simply instantiate the Swarmstar class with an id and goal. This will create a new swarmstar space in MongoDB and the first operation.
Following that, just keep feeding operations into the execute function and it will return the next operations to be executed.

Keep in mind that you shouldn't pass UserCommunication operations into the execute function. 
I've provided a template for how you may handle those in the user_communication_examples folder.
"""
from typing import List, Union
import inspect

from swarmstar.models import (
    SwarmOperation,
    SpawnOperation,
    SwarmstarSpace
)
from swarmstar.operations import (
    blocking,
    spawn,
    terminate,
    execute_action
)
from swarmstar.utils.database import MongoDBWrapper
from swarmstar.context import swarm_id_var

db = MongoDBWrapper()

class Swarmstar:
    def __init__(self, swarm_id: str):
        swarm_id_var.set(swarm_id)

    def instantiate(self, goal: str) -> SpawnOperation:
        """ Only call this function once at the start of each swarm """
        SwarmstarSpace.instantiate_swarmstar_space(swarm_id_var.get())

        root_spawn_operation = SpawnOperation(
            action_id='general/plan',
            message=goal
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

    def delete(self):
        """ Only call this function once at the end of each swarm """
        SwarmstarSpace.delete_swarmstar_space(swarm_id_var.get())
