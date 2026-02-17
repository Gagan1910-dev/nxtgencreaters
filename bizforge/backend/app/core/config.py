import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "BizForge AI"
    API_V1_STR: str = "/api/v1"
    # In a real app, these would come from env vars
    # IBM_GRANITE_KEY: str = os.getenv("IBM_GRANITE_KEY", "")
    # GROQ_API_KEY: str = os.getenv("GROQ_API_KEY", "")
    # HF_API_KEY: str = os.getenv("HF_API_KEY", "")

    class Config:
        env_file = ".env"
        case_sensitive = True
        extra = "ignore" # Ignore extra env vars not defined here

    # API Keys
    GROQ_API_KEY: str = os.getenv("GROQ_API_KEY", "")
    GROQ_MODEL: str = os.getenv("GROQ_MODEL", "llama-3.1-8b-instant")
    STABILITY_API_KEY: str = os.getenv("STABILITY_API_KEY", "")
    HF_API_KEY: str = os.getenv("HF_API_KEY", "")
    IBM_WATSONX_API_KEY: str = os.getenv("IBM_WATSONX_API_KEY", "")
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")

settings = Settings()
