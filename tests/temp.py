from pydantic import BaseModel


class temp(BaseModel):
    a: int
    b: int

gra = temp(a=1, b=2, c=3)

print(temp.model_validate(gra))