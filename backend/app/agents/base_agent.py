from abc import ABC, abstractmethod
from typing import Dict, Any
from app.core.config import settings

class BaseAgent(ABC):
    def __init__(self, name: str):
        self.name = name
        
        # Choose LLM provider based on settings
        if settings.USE_GROQ and settings.GROQ_API_KEY:
            from langchain_groq import ChatGroq
            self.llm = ChatGroq(
                model=settings.GROQ_MODEL,
                temperature=0.7,
                groq_api_key=settings.GROQ_API_KEY
            )
            print(f"Using Groq ({settings.GROQ_MODEL}) for {name} agent")
        else:
            from langchain_openai import ChatOpenAI
            self.llm = ChatOpenAI(
                model=settings.OPENAI_MODEL,
                temperature=0.7,
                openai_api_key=settings.OPENAI_API_KEY
            )
            print(f"Using OpenAI ({settings.OPENAI_MODEL}) for {name} agent")
    
    @abstractmethod
    async def process(self, state: Dict[str, Any]) -> Dict[str, Any]:
        pass