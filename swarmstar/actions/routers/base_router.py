"""
Routers are used to navigate a metadata tree to find a node.

Starting from a given root node, the router will step through the tree
using an LLM to make decisions until it reaches a leaf node.
"""
from pydantic import BaseModel
from typing import List
from abc import ABC, abstractmethod

from swarmstar.actions.base_action import BaseAction
from swarmstar.models import (
    BlockingOperation,
    BaseNode
)
from swarmstar.database import MongoDBWrapper
from swarmstar.utils.ai.instructor_models import NextPath

db = MongoDBWrapper()

class BaseMetadataTreeRouter(BaseAction, BaseModel, ABC):
    ROUTE_INSTRUCTIONS: str
    root_node_id: str

    @classmethod
    def main(self) -> BlockingOperation:
        return self._return_routing_blocking_operation(self.root_node_id)

    @BaseAction.receive_completion_handler
    def route(self, completion: NextPath, children_ids: List[str]):
        """ This function repeatedly gets called until we reach a leaf node. """
        if completion.index is not None:
            next_node = BaseNode.get(children_ids[completion.index])
            return self._return_routing_blocking_operation(next_node.id)
        else:
            self.handle_route_failure(completion.failure_message, children_ids)

    @abstractmethod
    def handle_route_failure(self, failure_message: str, option_ids: List[str]):
        """ Handle the case where there is no good path to take. """
        pass

    def _return_routing_blocking_operation(self, node_id: str):
        node = BaseNode.get(node_id)
        children = self._get_children(node)
        children_ids = [child.id for child in children]
        children_descriptions = self._get_children_descriptions(children)
        message = self._build_message(children_descriptions)
        return BlockingOperation(
            node_id=self.node.id,
            blocking_type="instructor_completion",
            args={"message": message},
            context={"instructor_model_name": "NextPath", "children_ids": children_ids},
            next_function_to_call="route"
        )

    def _get_children(self, node: BaseNode) -> List[BaseNode]:
        """ Get the children of a node from the database. """
        children = []
        for child_id in node.children_ids:
            children.append(BaseNode.get(child_id))
        return children

    def _build_message(self, children: List[BaseNode]) -> str:
        """ Get the descriptions of the children of a node. """
        options = [f"{i}. {child.name}: {child.description}" for i, child in enumerate(children)]
        options = "\n".join(options)
        message = self.node.message
        return (
            f"{self.ROUTE_INSTRUCTIONS}\n\n"
            f"Message to be routed: {message}\n\n"
            f"Options:\n"
            f"{options}"
        )
