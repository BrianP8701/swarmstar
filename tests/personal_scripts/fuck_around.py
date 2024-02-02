# # from aga_swarm.swarm.types import *

# # from pydantic import BaseModel, Field
# # from datetime import date


# # print(ActionMetadata.model_json_schema())
# # print(type(ActionMetadata.model_json_schema()))

# # pp = LifecycleCommand.EXECUTE

# # print(pp.name.title)


# # class DateRange(BaseModel):
# #     chain_of_thought: str = Field(
# #         description="Think step by step to plan what is the best time range to search in"
# #     )
# #     start: date
# #     end: date


# # class Query(BaseModel):
# #     rewritten_query: str = Field(
# #         description="Rewrite the query to make it more specific"
# #     )
# #     published_daterange: DateRange = Field(
# #         description="Effective date range to search in"
# #     )

# #     def report(self):
# #         dct = self.model_dump()
# #         dct["usage"] = self._raw_response.usage.model_dump()
# #         return dct
    
# # q = Query(
# #     rewritten_query="",
# #     published_daterange=DateRange(
# #         chain_of_thought="",
# #         start=date(2022, 1, 1),
# #         end=date(2022, 1, 1),
# #     ),
# # )

# # print(q.report())


# from typing import Annotated
# from pydantic import ValidationInfo, AfterValidator, BaseModel

# def citation_exists(v: str, info: ValidationInfo):
#     context = info.context
#     print(info)
#     print(v)
#     if context:
#         context = context.get("text_chunk")
#         if v not in context:
#             raise ValueError(f"Citation `{v}` not found in text, only use citations from the text.")
#     return v

# Citation = Annotated[str, AfterValidator(citation_exists)]


# class AnswerWithCitation(BaseModel):
#     answer: str
#     citation: Citation

# try:
#     AnswerWithCitation.model_validate(
#         {
#             "answer": "Blueberries are packed with protein",
#             "citation": "Blueberries contain high levels of protein",
#         },
#         context={"text_chunk": "Blueberries are very rich in antioxidants"},
#     )
# except Exception as e:
#     print(e)
    
    
# from pydantic import BaseModel, ValidationError
# from typing_extensions import Annotated
# from pydantic import AfterValidator

# def name_must_contain_space(v: str) -> str:
#     if " " not in v:
#         raise ValueError("Name must contain a space.")
#     return v.upper()

# class UserDetail(BaseModel):
#     age: int
#     name: Annotated[str, AfterValidator(name_must_contain_space)]

# person = UserDetail(age=29, name="Jason ")
# print(person)


# from pydantic import BaseModel, ValidationError, field_validator
# from pydantic.fields import Field

# blacklist = ["hurtt", "kill", "murder"]

# class Response(BaseModel):
#     message: str

#     @field_validator('message')
#     def message_cannot_have_blacklisted_words(cls, v: str) -> str:
#         for word in v.split(): 
#             if word.lower() in blacklist:
#                 raise ValueError(f"`{word}` was found in the message `{v}`")
#         return v

# k = Response(message="I will hurt him")

# print(k.message_cannot_have_blacklisted_words("buttcheeks"))



from pydantic import BaseModel
import os
from dotenv import load_dotenv
import pdb

from aga_swarm.utils.llm import completion

class UserInfo(BaseModel):
    name: str
    age: int
    gender: str



load_dotenv()
openai_key = os.getenv("OPENAI_API_KEY")


messages = [
    {
        "role": "user",
        "content": "I am 29 years old, male, and my name is Jason"
    }
]

resp = completion(messages, openai_key, UserInfo)
print(resp)
pdb.set_trace()
print(resp)
print(type(resp))