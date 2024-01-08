from settings import Settings
from openai import AsyncOpenAI

def get_openai_client():
    settings = Settings()
    return AsyncOpenAI(api_key=settings.OPENAI_API_KEY)