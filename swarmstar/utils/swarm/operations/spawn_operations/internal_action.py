from importlib import import_module
from typing import List, Union

from swarmstar.swarm.types import Action, SwarmConfig, SwarmNode, SwarmOperation


def execute_action(
    swarm: SwarmConfig, node: SwarmNode, action_metadata: Action
) -> Union[SwarmOperation, List[SwarmOperation]]:
    internal_action_path = action_metadata.internal_action_path
    action_name = action_metadata.name
    action_class = getattr(import_module(internal_action_path), action_name)
    action_instance = action_class(swarm=swarm, node=node)
    return action_instance.main()
