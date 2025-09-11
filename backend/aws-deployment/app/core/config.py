from pydantic_settings import BaseSettings
from typing import List, Optional

class Settings(BaseSettings):
    # App
    APP_NAME: str = "AgentPlanner"
    DEBUG: bool = True
    API_V1_STR: str = "/api/v1"
    
    # OpenAI
    OPENAI_API_KEY: str = ""
    OPENAI_MODEL: str = "gpt-3.5-turbo"
    
    # Groq (add these new fields)
    GROQ_API_KEY: Optional[str] = None
    USE_GROQ: bool = False
    GROQ_MODEL: str = "llama3-8b-8192"
    
    # CORS
    BACKEND_CORS_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:3001"]
    
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()