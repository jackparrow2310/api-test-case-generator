from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    """Application configuration"""
    openai_api_key: str
    openai_model: str = "gpt-4o"
    max_test_cases: int = 10
    temperature: float = 0.7
    
    class Config:
        env_file = ".env"

settings = Settings()