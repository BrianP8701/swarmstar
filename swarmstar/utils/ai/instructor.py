from typing import Dict, List, Type
import os
from dotenv import load_dotenv

import instructor
from pydantic import BaseModel
from openai import AsyncOpenAI

load_dotenv()
OPENAI_KEY = os.getenv("OPENAI_KEY")

class Instructor:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.aclient = instructor.apatch(AsyncOpenAI(api_key=OPENAI_KEY))
        return cls._instance

    async def completion(
        self,
        messages: List[Dict[str, str]],
        instructor_model: Type[BaseModel],
        max_retries: int = 3,
    ) -> Type[BaseModel]:
        """
        Most of you are likely familiar with tool calling with GPT4.

        This is just that but instead of passing a JSON string, we
        pass a Pydantic model, and it returns that Pydantic model.

        In addition, we can add retry mechanisms. This is all thanks to
        Jason Liu and his instructor package. Definitely recommend
        checking it out!

        https://github.com/jxnl/instructor

        Args:
        - messages: List[Dict[str, str]]: The messages to send to the model
        - instructor_model: Type[BaseModel]: The Pydantic model to return
        - max_retries: int: The maximum number of retries to attempt

        Returns:
        - Type[BaseModel]: The Pydantic model
        """
        task = self.aclient.chat.completions.create(
            model="gpt-4-1106-preview",
            messages=messages,
            response_model=instructor_model,
            temperature=0.0,
            seed=69,
            max_retries=max_retries,
        )

        return await task