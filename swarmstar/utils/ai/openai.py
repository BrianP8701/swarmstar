from typing import Dict, List
import os
from dotenv import load_dotenv

from openai import AsyncOpenAI

load_dotenv()
OPENAI_KEY = os.getenv("OPENAI_KEY")

class OpenAI:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.aclient = AsyncOpenAI(api_key=OPENAI_KEY)
        return cls._instance

    async def completion(
        self,
        messages: List[Dict[str, str]]
    ) -> str:
        task = self.aclient.chat.completions.create(
            model="gpt-4-1106-preview",
            messages=messages,
            temperature=0.0,
            seed=69
        )

        completion = await task
        return completion.choices[0].message.content
