"""
The swarm util space metadata has a simlar but different role to 
the action space metadata:

    (1) To allow the swarm to organize and search for utils
    (2) Describe how to interact with the utils

Swarm utils are just swarm specific functions. They may be
used in the construction of actions.

For now we assume all utils are internal to the package.
"""
from typing import Dict, List, Optional

from pydantic import BaseModel, Field
from typing_extensions import Literal

from swarmstar.utils.misc.generate_uuid import generate_uuid
from swarmstar.utils.data import MongoDBWrapper
from swarmstar.models.internal_metadata import SwarmstarInternal

db = MongoDBWrapper()

class UtilMetadata(BaseModel):
    id: Optional[str] = Field(default_factory=lambda: generate_uuid('util'))
    type: Literal["internal_folder", "internal_function"]
    name: str
    description: str
    parent: str
    children: List[str] = []
    metadata: Dict[str, str]

    @staticmethod
    def get(util_id: str) -> 'UtilMetadata':
        try:
            util_metadata = db.get("util_metadata", util_id)
            if util_metadata is None:
                raise ValueError(
                    f"This util id: `{util_id}` does not exist in external util space."
                )
        except:
            try:
                util_metadata = SwarmstarInternal.get_util_metadata(util_id)
                if util_metadata is None:
                    raise ValueError(
                        f"This util id: `{util_id}` does not exist in internal util space."
                    )
            except:
                raise ValueError(
                    f"This util id: `{util_id}` does not exist in both internal and external util spaces."
                )

        type_mapping = {

        }
        util_type = util_metadata["type"]
        if util_type in type_mapping:
            return type_mapping[util_type](**util_metadata)
        return UtilMetadata(**util_metadata)
