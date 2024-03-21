from pydantic import BaseModel
import asyncio
from swarmstar.utils.ai import Instructor
from swarmstar.utils.ai.instructor_models import QuestionWrapper


instructor = Instructor()

class Test(BaseModel):
    number: int


messages = [{
    "role": "system",
    "content": "What is 2 + 2?"
}]

asyncio.run(instructor.completion(messages=messages, instructor_model=QuestionWrapper(Test)))
