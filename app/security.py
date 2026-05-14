from fastapi import Security, HTTPException, status
from fastapi.security.api_key import APIKeyHeader
from app.config import settings

api_key_header = APIKeyHeader(name="x-api-key", auto_error=False)

async def validate_api_key(api_key: str = Security(api_key_header)):
    if api_key == settings.MASTER_API_KEY:
        return api_key
    
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid or missing Master API Key"
    )
