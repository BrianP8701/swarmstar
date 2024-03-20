import asyncio
from pydantic import BaseModel






class Test(BaseModel):
    test: str

test = Test(test="test")

print(test.lala)