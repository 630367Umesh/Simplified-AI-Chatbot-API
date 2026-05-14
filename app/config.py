import os
import json
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    # Security
    MASTER_API_KEY: str = os.getenv("MASTER_API_KEY", "default-master-key")
    
    # LLM Provider: Gemini
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")
    GEMINI_MODEL: str = os.getenv("GEMINI_MODEL", "gemini-1.5-flash")
    
    # LLM Provider: Groq
    GROQ_API_KEY: str = os.getenv("GROQ_API_KEY", "")
    GROQ_MODEL: str = os.getenv("GROQ_MODEL", "llama-3.1-8b-instant")
    
    # LLM Provider: Llama (Ollama / Local / Hosted)
    LLAMA_API_URL: str = os.getenv("LLAMA_API_URL", "http://localhost:11434/api/generate")
    LLAMA_MODEL: str = os.getenv("LLAMA_MODEL", "llama3.1")
    
    # App Settings
    PROJECT_NAME: str = "Simplified AI Chatbot API"
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "production")
    
    @property
    def ALLOWED_ORIGINS(self) -> list:
        origins = os.getenv("ALLOWED_ORIGINS", '["*"]')
        try:
            return json.loads(origins)
        except json.JSONDecodeError:
            return [origin.strip() for origin in origins.split(",")]

settings = Settings()
