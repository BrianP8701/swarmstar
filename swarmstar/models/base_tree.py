from pydantic import BaseModel
from abc import ABC

from swarmstar.database import MongoDBWrapper
from swarmstar.models.base_node import BaseNode

db = MongoDBWrapper()

class BaseTree(ABC, BaseModel):
    """
    We use trees quite a lot in swarmstar. The actual swarm's nodes are stored in a tree.
    Actions and memory are stored in a tree. The tree is a very useful data structure for
    organizing data in a way that's easy to traverse and understand. It's also naturally
    efficient and scalable.

    This class just provides some common functions that are shared by all trees.
    """
    collection: str # Collection name in the database

    def is_external(node: BaseNode):
        """
        Checks if this node is external, meaning it's stored in the database, not inside the package.
        Internal refers to stuff stored inside the swarmstar package, in a file or internal sqlite database.

        The base tree could contain swarm or metadata nodes.
        Swarm nodes are always stored externally, tied to an instance of the swarm.
        Metadata nodes can be internal and portal nodes close the gap between internal and external.
        """
        if node.collection == "swarm_nodes": return True
        return not node.get("internal", False) or node.get("type", None) == "portal"

    @classmethod
    def get_root_node_id(cls, swarm_id: str) -> str:
        # For simplicity i have a strict format for ids
        if cls.collection == "swarm_nodes":
            return f"{swarm_id}_n0"
        # The memory and action space always start internally with a node called "root"
        # Portal nodes connect the internal and external space
        return "root"

    @classmethod
    def clone(cls, old_swarm_id: str, swarm_id: str) -> None:
        """ Clones every node in the tree under a new swarm id in the database. """
        root_node_id = cls.get_root_node_id(old_swarm_id)

        def recursive_helper(node_id):
            node = BaseNode.get(node_id)
            is_external = cls.is_external(node)

            if node.children_ids:
                for i, child_id in enumerate(node.children_ids):
                    recursive_helper(child_id)
                    if is_external:
                        parts = child_id.split("_", 1)
                        node.children_ids[i] = f"{swarm_id}_{parts[1]}"

            if is_external:
                parts = node.id.split("_", 1)
                node.id = f"{swarm_id}_{parts[1]}"
                # If the node has a parent and is not a portal node, change the parent id
                if node.parent_id and not node.type == "portal":
                    parts = node.parent_id.split("_", 1)
                    node.parent_id = f"{swarm_id}_{parts[1]}"
                db.insert(cls.collection, node)

        recursive_helper(root_node_id)

    @classmethod
    def delete(cls, swarm_id: str) -> None:
        """ Deletes every node in the tree from the database. """
        root_node_id = cls.get_root_node_id(swarm_id)
        
        def recursive_helper(node_id):
            node = BaseNode.get(node_id)
            if node.children_ids:                    
                for child_id in node.children_ids:
                    recursive_helper(child_id)
            if cls.is_external(node):
                db.delete(cls.collection, node_id)

        recursive_helper(root_node_id)
