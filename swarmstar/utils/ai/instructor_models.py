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

class QuestionWrapper(BaseModel):
    questions: List[str] = Field(..., description="CRITICAL: You must only make decisions or plan when you feel you have all the necessary context. Otherwise, you must ask questions to gather the necessary context.")

class DecomposeDirectiveModel(QuestionWrapper):
    subdirectives: Optional[List[str]] = Field(
        None,
        description="List of subdirectives to be executed in parallel, if you have no questions.",
    )


class NextPath(BaseModel):
    index: Optional[int] = Field(
        None, description="Index of the best path to take"
    )
    failure_message: Optional[str] = Field(
        None,
        description="There's no good path to take. Describe what you're looking for in detail.",
    )


class InitialQuestionAskerConversationState(QuestionWrapper):
    persisted_context: str = Field(
        ...,
        description="A concise and compact representation of the necessary information to persist through the conversation.",
    )
    chat_name: str = Field(..., description="A 2-4 word name for the conversation")


class QuestionAskerConversationState(QuestionWrapper):
    persisted_context: str = Field(
        ...,
        description="A concise and compact representation of the necessary information to persist through the conversation.",
    )
    report: str = Field(
        ...,
        description="Concise and comprehensive report of answers to our questions and supporting context.",
    )


class ConfirmDirectiveModel(QuestionWrapper):
    is_complete: bool = Field(
        ..., description="Whether the directive is complete or not."
    )
