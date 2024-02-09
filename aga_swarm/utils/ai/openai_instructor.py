from openai import OpenAI
from typing import List, Dict, Type
from pydantic import BaseModel
import instructor

def completion(messages: List[Dict[str, str]], openai_key: str, instructor_model: Type[BaseModel], max_retries: int = 3) -> Type[BaseModel]:
    '''
    Most of you are likely familiar with tool calling with GPT4.
    
    This is just that but instead of passing a JSON string, we
    pass a Pydantic model, and it returns that Pydantic model.
    
    In additon we can add retry mechanisms. This is all thanks to 
    Jason Liu and his instructor package. Definitely recommend
    checking it out!
    
    https://github.com/jxnl/instructor

    Args:
    - messages: List[Dict[str, str]]: The messages to send to the model
    - openai_key: str: The OpenAI API key
    - model: Type[BaseModel]: The Pydantic model to return
    - max_retries: int: The maximum number of retries to attempt
    
    Returns:
    - Type[BaseModel]: The Pydantic model
    '''
    client = instructor.patch(OpenAI(api_key=openai_key))
    return client.chat.completions.create(model='gpt-4-1106-preview', 
                                          messages=messages, 
                                          response_model=instructor_model, 
                                          temperature=0.0, 
                                          seed=69, 
                                          max_retries=max_retries)
