from openai import OpenAI
from typing import List, Dict, Type
from pydantic import BaseModel
import instructor

def completion(messages: List[Dict[str, str]], openai_key: str, model: Type[BaseModel], max_retries: int) -> Type[BaseModel]:
    '''
    Most of you are likely familiar with tool calling with GPT4.
    
    This is just that but instead of passing a JSON string, we
    pass a Pydantic model, and it returns that Pydantic model.
    
    In additon we can add retry mechanisms. This is all thanks to 
    Jason Liu and his instructor package. Definitely recommend
    checking it out!
    
    https://github.com/jxnl/instructor
    '''
    client = instructor.patch(OpenAI(api_key=openai_key))
    return client.chat.completions.create(model='gpt-4-1106-preview', 
                                          messages=messages, 
                                          response_model=model, 
                                          temperature=0.0, 
                                          seed=69, 
                                          max_retries=max_retries)
