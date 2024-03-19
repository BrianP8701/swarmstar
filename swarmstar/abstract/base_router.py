# from pydantic import BaseModel, Field
# from typing import Optional

# from swarmstar.abstract.base_action import BaseAction
# from swarmstar.models import (
#     ActionFolder,
#     BlockingOperation,
#     NodeEmbryo,
#     SpawnOperation,
#     SwarmOperation,
#     ActionMetadata
# )
# from swarmstar.

# db = MongoDBWrapper()

# class BaseMetadataTreeRouter(BaseAction, BaseModel):
#     ROUTE_INSTRUCTIONS: str
#     root_node_id: str
#     collection: str
#     class NextPath(BaseModel):
#         index: Optional[int] = Field(None, description="Index of the best path to take")
#         failure_message: Optional[str] = Field(None, description="Failure message describing precisely what you failed to find.")

#     @classmethod
#     def main(self) -> BlockingOperation:
#         root = 

