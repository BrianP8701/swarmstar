"""
Given a directive, the router agent uses an LLM to navigate the action space 
through its metadata to decide what action to take. If there is no good action
path to take, the router agent will describe what type of action is needed in detail.
"""
from typing import List

from swarmstar.models import SpawnOperation
from swarmstar.actions.routers.base_router import BaseMetadataTreeRouter

class RouteAction(BaseMetadataTreeRouter):
    ROUTE_INSTRUCTIONS = (
        "Decide what action path to take based on the directive and the available actions. "
        "If there is no good action path to take, describe what type of action is needed "
        "in detail in the failure message, and leave index empty."
    )
    root_node_id = "general"

    def handle_route_success(self, node_id: str):
        return SpawnOperation(
            parent_id=self.node.id,
            action_id=node_id,
            message=self.node.message,
            context=self.node.context
        )

    def handle_route_failure(self, failure_message: str, option_ids: List[str]):
        # TODO: Implement this when we have a better idea of how to handle this.
        raise ValueError(f"RouteAction failed: {failure_message}")