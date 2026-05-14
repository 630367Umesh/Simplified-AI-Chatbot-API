from fastapi import APIRouter, Depends
from app.schemas.chat_schema import ChatRequest, ChatResponse
from app.services.chatbot_service import chatbot_service
from app.security import validate_api_key

router = APIRouter()

@router.post("/v1/chat", response_model=ChatResponse)
async def chat_endpoint(
    payload: ChatRequest, 
    api_key: str = Depends(validate_api_key)
):
    """
    Main chat endpoint. 
    Requires x-api-key header matching MASTER_API_KEY.
    """
    reply = await chatbot_service.get_chat_response(
        message=payload.message,
        provider=payload.provider
    )
    
    return ChatResponse(
        success=True,
        provider=payload.provider,
        reply=reply
    )
