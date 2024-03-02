from pydantic import BaseModel, field_validator
from typing import Optional
from swarmstar.utils.misc.uuid import generate_uuid

class temp(BaseModel):
    a: int
    b: int
    id: Optional[str] = generate_uuid('temp')
    
    @field_validator('id')
    @classmethod
    def create_id(cls, v: str) -> str:
        return '123'
    


gra = temp(
    a=1,
    b=2,
    id='123'
)

model = temp.model_validate(gra)
print(model)

