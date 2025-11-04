from pydantic_settings import BaseSettings
from typing import List, Optional
import os

class Settings(BaseSettings):
    # App
    APP_NAME: str = "AgentPlanner"
    DEBUG: bool = True
    API_V1_STR: str = "/api/v1"
    
    # OpenAI
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    OPENAI_MODEL: str = "gpt-3.5-turbo"
    
    # Groq
    GROQ_API_KEY: Optional[str] = os.getenv("GROQ_API_KEY", None)
    USE_GROQ: bool = True
    GROQ_MODEL: str = "llama-3.3-70b-versatile"
    
    # CORS
    BACKEND_CORS_ORIGINS: List[str] = [
        "http://localhost:3000",
        "https://agentplanner.web.app",
        "https://agentplanner.firebaseapp.com"
    ]
    
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()
