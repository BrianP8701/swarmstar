"""
The actions that create blocking operations using instructor need to pass
the pydantic model. However, the pydantic model can't be serialized and 
deserialized. (There are serialization methods but no common deserialization methods)

So instead we'll store all the pydantic models in this file and import them, 
passing the name of the model as a string in the blocking operation.
"""

from typing import List, Optional

from pydantic import BaseModel, Field


class DecomposeDirectiveModel(BaseModel):
    scrap_paper: Optional[str] = Field(
        None,
        description="Scrap paper for notes, planning etc. Use this space to think step by step. (optional)",
    )
    questions: Optional[List[str]] = Field(
        None, description="Questions you need answered before decomposition."
    )
    subdirectives: Optional[List[str]] = Field(
        None,
        description="List of subdirectives to be executed in parallel, if you have no questions.",
    )


class NextActionPath(BaseModel):
    index: Optional[int] = Field(
        None, description="Index of the best action path to take"
    )
    failure_message: Optional[str] = Field(
        None,
        description="There's no good action path to take. Describe what type of action is needed in detail.",
    )


class QuestionAskerConversationState(BaseModel):
    questions: List[str] = Field(..., description="List of questions we need answered")
    persisted_context: str = Field(
        ...,
        description="A concise and compact representation of the necessary information to persist through the conversation.",
    )
    report: str = Field(
        ...,
        description="Concise and comprehensive report of answers to our questions and supporting context.",
    )


class AgentMessage(BaseModel):
    content: str = Field(..., description="The message to send to the user.")


class FinalReport(BaseModel):
    report: str = Field(
        ...,
        description="Concise and comprehensive report of answers to our questions and supporting context.",
    )


class ConfirmCompletionModel(BaseModel):
    is_complete: bool = Field(
        ..., description="Whether the directive is complete or not."
    )
    message: Optional[str] = Field(
        None, description="If the directive is not complete, this message will be sent back to the decompose directive node."
    )