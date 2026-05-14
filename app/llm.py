import google.generativeai as genai
from groq import Groq
import httpx
import asyncio
from app.config import settings
from app.utils.logger import logger

class LLMRouter:
    def __init__(self):
        # Gemini Init
        genai.configure(api_key=settings.GEMINI_API_KEY)
        self.gemini_model = genai.GenerativeModel(settings.GEMINI_MODEL)
        
        # Groq Init
        self.groq_client = Groq(api_key=settings.GROQ_API_KEY)
        
        # System Prompt
        self.system_prompt = "You are a professional AI assistant. Provide accurate and concise responses."

    async def chat_gemini(self, prompt: str):
        try:
            response = await asyncio.to_thread(
                self.gemini_model.generate_content,
                prompt
            )
            return response.text, settings.GEMINI_MODEL
        except Exception as e:
            logger.error(f"Gemini Error: {e}")
            raise e

    async def chat_groq(self, prompt: str):
        try:
            response = await asyncio.to_thread(
                self.groq_client.chat.completions.create,
                model=settings.GROQ_MODEL,
                messages=[{"role": "user", "content": prompt}]
            )
            return response.choices[0].message.content, settings.GROQ_MODEL
        except Exception as e:
            logger.error(f"Groq Error: {e}")
            raise e

    async def chat_llama(self, prompt: str):
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    settings.LLAMA_API_URL,
                    json={
                        "model": settings.LLAMA_MODEL,
                        "prompt": prompt,
                        "stream": False
                    },
                    timeout=60.0
                )
                data = response.json()
                # Assuming Ollama style response
                return data.get("response", "No response from Llama"), settings.LLAMA_MODEL
        except Exception as e:
            logger.error(f"Llama Error: {e}")
            raise e

    async def get_response(self, provider: str, message: str):
        provider = provider.lower()
        if provider == "gemini":
            return await self.chat_gemini(message)
        elif provider == "llama":
            return await self.chat_llama(message)
        else: # Default to groq
            return await self.chat_groq(message)

llm_router = LLMRouter()
