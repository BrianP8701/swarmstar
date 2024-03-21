"""
Routers are used to navigate a metadata tree to find a node.

This is a base class to easily create routers over any MetadataTree, 
starting from any chosen root node.
"""
from pydantic import BaseModel
from typing import List, Dict, Any
from abc import ABC, abstractmethod

from swarmstar.actions.base_action import BaseAction
from swarmstar.models import (
    BlockingOperation,
    BaseNode
)
from swarmstar.utils.database import MongoDBWrapper
from swarmstar.utils.ai.instructor_models import NextPath

db = MongoDBWrapper()

class BaseMetadataTreeRouter(BaseAction, BaseModel, ABC):
    ROUTE_INSTRUCTIONS: str
    root_node_id: str

    @classmethod
    def main(self) -> BlockingOperation:
        return self.route(self.root_node_id)

    @BaseAction.receive_instructor_completion_handler
    def handle_routing_decision(self, completion: NextPath, context: Dict[str, Any]):
        """ This function repeatedly gets called until we reach a leaf node. """
        children_ids = context["children_ids"]
        if completion.index is not None:
            next_node = BaseNode.get(children_ids[completion.index])
            if next_node.is_folder:
                return self.route(next_node.id)
            else:
                return self.handle_route_success(next_node.id)
        else:
            self.handle_route_failure(completion.failure_message, children_ids)

    @abstractmethod
    def handle_route_failure(self, failure_message: str, option_ids: List[str]):
        """ Handle the case where there is no good path to take. """
        pass

    @abstractmethod
    def handle_route_success(self, node_id: str):
        """ Handle the case where we have reached a leaf node. """
        pass

    def route(self, node_id: str):
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
            next_function_to_call="handle_routing_decision"
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
