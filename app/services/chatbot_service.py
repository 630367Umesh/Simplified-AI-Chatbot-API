from app.llm import llm_router
from app.utils.logger import logger
import time

class ChatbotService:
    @staticmethod
    async def get_chat_response(message: str, provider: str):
        start_time = time.time()
        try:
            reply, model_used = await llm_router.get_response(provider, message)
            duration = time.time() - start_time
            logger.info(f"Request handled by {provider} ({model_used}) in {duration:.2f}s")
            return reply
        except Exception as e:
            logger.error(f"ChatbotService Error: {e}")
            raise e

chatbot_service = ChatbotService()
