'''
the settings object contains global constants defined in the .env file

the .env file contains my openai api key as well as relative local paths the swarm uses
'''

from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    OPENAI_API_KEY: str
    FIRESTORE_CREDENTIALS: str

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'
