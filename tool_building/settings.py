from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    OPENAI_API_KEY: str
    AGENTS_PATH: str
    NODE_SCRIPTS_PATH: str
    SYNTHETIC_CODE_PATH: str
    AUTONOMOUS_SCRIPT_TESTS_PATH: str
    MANUAL_TESTING_GROUND_FOLDER_PATH: str
    MANUAL_SCRIPT_TESTS_PATH: str

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'
