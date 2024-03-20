from swarmstar.models.base_tree import BaseTree
from swarmstar.database.internal import get_internal_sqlite
from swarmstar.database import MongoDBWrapper

db = MongoDBWrapper()

class MetadataTree(BaseTree):
    
    @classmethod
    def instantiate(cls, swarm_id: str) -> None:
        """
        Only call this once when a swarm instance is created.
        
        Swarmstar comes with a default action and memory metadata tree. When 
        a swarm instance is created, it'll need to be able to access the default 
        action and memory metadata tree but also be able to dynamically add 
        actions and memories. 
        
        It would be wasteful to copy the entire default action and memory 
        metadata tree each time, as they're immutable. Rather, a select 
        few nodes, coined "portal nodes", which are folder nodes where we may 
        attach connections to external nodes, will be cloned.
        """
        internal_root_node_id = "root"
        node = get_internal_sqlite(cls.collection, internal_root_node_id)
        
        def recursive_helper(node):
            if node["type"] == "portal":
                node_id = f"{swarm_id}_{node['id']}"
                db.insert(cls.collection, node_id, node)
            if node.get("children_ids", None):
                for child_id in node["children_ids"]:
                    child_node = get_internal_sqlite(cls.collection, child_id)
                    recursive_helper(child_node)

        recursive_helper(node)

