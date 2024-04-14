"""
Most of you are likely familiar with tool calling with GPT4.

This is just that but instead of passing a JSON string, we
pass a Pydantic model, and it returns that Pydantic model.

In addition, we can add retry mechanisms. This is all thanks to
Jason Liu and his instructor package. Definitely recommend
checking it out!

https://github.com/jxnl/instructor

In this module we define all the Pydantic models that are used in 
the instructor module.

Pydantic models can't be serialized and turned back into Pydantic models
so we define them here, and pass around instructor model names as strings
in swarm operations.
"""

from typing import List, Optional

from pydantic import BaseModel, Field

class AskQuestions(BaseModel):
    shared_context_for_questions: Optional[str] = Field(None, description="Context shared with all questions if you have questions, otherwise None")
    questions: Optional[List[str]] = Field(None, description="List of questions to ask if you have questions, otherwise None")

class NextPath(BaseModel):
    index: Optional[int] = Field(
        None, description="Index of the best path to take"
    )
    failure_message: Optional[str] = Field(
        None,
        description="There's no good path to take. Describe what you're looking for in detail.",
    )
