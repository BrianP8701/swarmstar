"""
Base class for nodes.

Swarm nodes, action metadata nodes and memory metadata nodes are all derived from this class.
"""
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any, TypeVar

from swarmstar.utils.data import MongoDBWrapper
from swarmstar.models.internal_metadata import get_internal_sqlite
from swarmstar.context import swarm_id_var

db = MongoDBWrapper()

T = TypeVar('T', bound='BaseNode')

class BaseNode(BaseModel):
    """ Base class for nodes. """
    id: str 
    name: str
    parent_id: Optional[str] = None
    children_ids: Optional[List[str]] = None
    collection: str = Field(exclude=True)  # Collection name in the database

    @classmethod
    def get(cls, node_id: str) -> Dict[str, Any]:
        """
        The base class returns a dict. Perform validation in the derived classes.

        If the collection is "swarm_nodes", retrieve from the mongodb database.

        Otherwise, it is a metadata node, which means it can be internal or external.
        Try to retrieve from the internal sqlite database. If not found,
        check the mongodb database. If not found in either, raise an error.

        If found internally and of type "portal", prepend the node_id with
        the swarm_id and retrieve from the mongodb database.
        """
        if cls.collection == "swarm_nodes":
            return db.get(cls.collection, node_id)
        else:
            try:
                node = get_internal_sqlite(cls.collection, node_id)
                if node["type"] == "portal":
                    node_id = f"{swarm_id_var.get()}_{node_id}"
                    node = db.get(cls.collection, node_id)
                return node
            except:
                try:
                    return db.get(cls.collection, node_id)
                except:
                    raise ValueError(f"Node {node_id} not found in {cls.collection}")

    @classmethod
    def delete(cls, node_id: str) -> None:
        """ Deletes node from the database."""
        db.delete(cls.collection, node_id)

    @classmethod
    def update(cls, node_id: str, updated_values: Dict[str, Any]) -> None:
        """ Updates node in the database with updated values."""
        db.update(cls.collection, node_id, updated_values)

    @classmethod
    def replace(cls, node_id: str, new_node: T) -> None:
        """ Replaces node in the database with new node."""
        db.replace(cls.collection, node_id, new_node.model_dump())

    def insert(self) -> None:
        """ Inserts a node to the database. Raises an error if the node already exists. """
        db.insert(self.collection, self.id, self.model_dump())

    def clone(self, swarm_id: str) -> None:
        """ Clones this node under a new swarm id and saves it to the database. """
        parts = self.id.split("_")
        new_id = f"{swarm_id}_{parts[1]}"
        self.id = new_id
        self.insert()
