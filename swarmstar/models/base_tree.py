from pydantic import BaseModel
from abc import ABC

from swarmstar.utils.database import MongoDBWrapper
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
        return not node.read("internal", False) or node.get("portal", False)

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

        batch_copy_payload = [[], []] # [old_ids, new_ids]
        batch_update_payload = {} # {new_id: {parent_id: "", children_ids: []}} 

        def recursive_helper(node_id):
            node = BaseNode.read(node_id)
            is_external = cls.is_external(node)

            if node.children_ids:
                for i, child_id in enumerate(node.children_ids):
                    recursive_helper(child_id)
                    if is_external:
                        parts = child_id.split("_", 1)
                        node.children_ids[i] = f"{swarm_id}_{parts[1]}"

            if is_external:
                old_id = node.id
                parts = node.id.split("_", 1)
                node.id = f"{swarm_id}_{parts[1]}"
                # If the node has a parent and is not a portal node, change the parent id
                if node.parent_id and not node.get("portal", False):
                    parts = node.parent_id.split("_", 1)
                    node.parent_id = f"{swarm_id}_{parts[1]}"
                batch_copy_payload[0].append(old_id)
                batch_copy_payload[1].append(node.id)
                batch_update_payload[node.id] = {"parent_id": node.parent_id, "children_ids": node.children_ids}

        recursive_helper(root_node_id)

        if batch_copy_payload:
            db.batch_copy(cls.collection, batch_copy_payload)
        if batch_update_payload:
            db.batch_update(cls.collection, batch_update_payload)

    @classmethod
    def delete(cls, swarm_id: str) -> None:
        """ Deletes every node in the tree from the database. """
        root_node_id = cls.get_root_node_id(swarm_id)
        
        batch_delete_payload = []
        
        def recursive_helper(node_id):
            node = BaseNode.read(node_id)
            if node.children_ids:                    
                for child_id in node.children_ids:
                    recursive_helper(child_id)
            if cls.is_external(node):
                batch_delete_payload.append(node.id)

        recursive_helper(root_node_id)
        
        if batch_delete_payload:
            db.batch_delete(cls.collection, batch_delete_payload)
