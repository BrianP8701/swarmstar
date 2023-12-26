from pydantic import BaseModel
from typing import Optional, List

class Node(BaseModel):
    id: int
    type: str
    data: dict
    parent: Optional['Node'] = None
    children: List['Node'] = []
    output: Optional[dict] = None

    class Config:
        arbitrary_types_allowed = True
        validate_assignment = True
        allow_population_by_field_name = True
          
    def jsonify(self):
        return {
            "task_type": self.type,
            "parent": self.parent,
            "children": self.children,
            "input_data": self.data,
            "output_data": self.output
        }