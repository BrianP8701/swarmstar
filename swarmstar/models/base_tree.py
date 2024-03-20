from pydantic import BaseModel
from abc import ABC

from swarmstar.database import MongoDBWrapper
from swarmstar.models.base_node import BaseNode

db = MongoDBWrapper()

class BaseTree(ABC, BaseModel):
    collection: str # Collection name in the database

    def is_external(node: BaseNode):
        """
        Checks if this node is external, meaning it's stored in the database.

        The base tree could contain swarm or metadata nodes.
        Swarm nodes are always stored externally, tied to an instance of the swarm.
        Metadata nodes are stored externally if they are not internal or if they are a portal
        """
        if node.collection == "swarm_nodes": return True
        return not node.get("internal", False) or node.get("type", None) == "portal"

    def clone(self, old_swarm_id: str, swarm_id: str) -> None:
        """ Clones every node in the tree under a new swarm id in the database. """
        root_node_id = f"{old_swarm_id}_{self.collection}_0"
        if not db.exists(self.collection, root_node_id):
            raise ValueError(f"In attempt to clone metadata tree {self.collection}, root node {root_node_id} does not exist.")

        def recursive_helper(node_id):
            node: dict = db.get(self.collection, node_id)
            is_clonable = self.is_external(node)
                           
            for i, child_id in enumerate(node["children_ids"]):
                recursive_helper(child_id)
                if is_clonable:
                    parts = child_id.split("_", 1)
                    node["children_ids"][i] = f"{swarm_id}_{parts[1]}"
            if is_clonable:
                parts = node["id"].split("_", 1)
                node["id"] = f"{swarm_id}_{parts[1]}"
                # If a node is a portal, it's parent is internal.
                if node.get("parent_id", None) and not node["type"] == "portal":
                    parts = node["parent_id"].split("_", 1)
                    node["parent_id"] = f"{swarm_id}_{parts[1]}"
                db.insert(self.collection, node)

        recursive_helper(root_node_id)

    def delete(self, swarm_id: str) -> None:
        """ Deletes every node in the tree from the database. """
        root_node_id = f"{swarm_id}_{self.collection}_0"
        if not db.exists(self.collection, root_node_id):
            raise ValueError(f"In attempt to delete metadata tree {self.collection}, root node {root_node_id} does not exist.")
        
        def recursive_helper(node_id):
            node: dict = db.get(self.collection, node_id)
            if node.get("children_ids", None):                    
                for child_id in node["children_ids"]:
                    recursive_helper(child_id)
            if self.is_external(node):
                db.delete(self.collection, node_id)

        recursive_helper(root_node_id)
