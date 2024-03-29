"""
The swarm consists of nodes. Each node is given a message 
and a preassigned action they must execute.
"""
from typing import Any, Dict, List, Optional, ClassVar
from enum import Enum
from pydantic import Field

from swarmstar.models.base_node import BaseNode
from swarmstar.utils.misc.ids import get_available_id

# Each termination policy has a unique handler in swarmstar/swarm_operations/termination_operations/main.py
class TerminationPolicies(Enum):
    SIMPLE = "simple"
    CONFIRM_DIRECTIVE_COMPLETION = "confirm_directive_completion"
    CUSTOM_TERMINATION_HANDLER = "custom_termination_handler"

class SwarmNode(BaseNode):
    id: Optional[str] = Field(default_factory=lambda: get_available_id("swarm_nodes"))
    collection: ClassVar[str] = "swarm_nodes"
    type: str    # Swarm nodes are classified by their action id
    message: str
    alive: bool = True
    termination_policy: TerminationPolicies = TerminationPolicies.SIMPLE
    developer_logs: List[Any] = []              # Logs storing all messages sent to and received from an ai throughout the action's execution.
    report: Optional[str] = None                    # We should look at the node and see like, "Okay, thats what this node did." 
    execution_memory: Optional[Dict[str, Any]] = {}     # This is where a node can store memory during the execution of an action.
    context: Optional[Dict[str, Any]] = {}          # This is where certain nodes can store extra context about themselves.

    @classmethod
    def read(cls, node_id: str) -> 'SwarmNode':
        swarm_node_dict = super().get_node_dict(node_id)
        return cls(**swarm_node_dict)

    def log(self, log_dict: Dict[str, Any], index_key: List[int] = None) -> List[int]:
        """
        This function appends a log to the developer_logs list in a node or a nested list 
        within developer_logs.

        The log_dict should have the following format:
        {
            "role": (swarmstar, system, ai or user),
            "content": "..."
        }
        
        If you are not doing parallel logs, you can ignore the index_key parameter.
        Parallel logs are logs that were performed in parallel. For example, if within 
        one node we have multiple conversations in parallel, we don't want these to 
        overlap in the logs.
        
        Example:

        [log0, log1, log2, [log3.0, log3.1, log3.2], log4]
            log3.0, log3.1, log3.2 are grouped.

        or even,

        [log0, log1, [[log2.0.0, log2.0.1, log2.0.2], [log2.1.0, log2.1.1]], log3]
            log2.0.0, log2.0.1, log2.0.2 are grouped.
            log2.1.0, log2.1.1 are grouped.
            log2.0 and log2.1 are performed in parallel.

        If index_key is None, the log will be appended to the developer_logs list.
        If an index_key is provided, the log will be appended to the nested list at the index_key.

        The function can create a new empty list and add the log if the list doesn't exist,
        but it can only create one list at a time. If an attempt is made to create more than one list
        at a time, an error will be raised.

        :param log_dict: A dictionary representing the log to be added.
        :param index_key: A list of integers representing the index path to the nested list where the log should be added.
        :raises ValueError: If an attempt is made to create more than one list at a time.

        :return: The index_key of the log that was added.
        """
        if index_key is None:
            self.developer_logs.append(log_dict)
            return_index_key = [len(self.developer_logs) - 1]
        else:
            nested_list = self.developer_logs
            for i, index in enumerate(index_key):
                if index > len(nested_list):
                    raise IndexError(f"Index {index} is out of range for the current list. {nested_list}")
                if i == len(index_key) - 1:
                    if len(nested_list) == index:
                        nested_list.append([log_dict])
                        return_index_key = index_key + [0]
                    elif isinstance(nested_list[index], list):
                        nested_list[index].append(log_dict)
                        return_index_key = index_key + [len(nested_list[index]) - 1]
                    else:
                        nested_list[index] = [nested_list[index], log_dict]
                        return_index_key = index_key + [1]
                else:
                    if isinstance(nested_list[index], list):
                        nested_list = nested_list[index]
                    else:
                        raise ValueError("Invalid index_key. Cannot traverse non-list elements.")
        SwarmNode.replace(self.id, self)
        return return_index_key
