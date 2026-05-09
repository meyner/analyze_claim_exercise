import os
from pydantic_settings import BaseSettings, SettingsConfigDict

# Get the directory where config.py is located
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

class Settings(BaseSettings):
    gemini_api_key: str = ""
    gemini_model: str = "gemini-2.5-flash"
    
    model_config = SettingsConfigDict(
        env_file=os.path.join(BASE_DIR, ".env.local"),
        env_file_encoding="utf-8",
        extra="ignore"
    )

settings = Settings()
