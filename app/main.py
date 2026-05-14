from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, Response
import uvicorn

from app.config import settings
from app.schemas.chat_schema import HealthResponse
from app.middleware import LoggingMiddleware
from app.routes import chat

app = FastAPI(
    title=settings.PROJECT_NAME,
    version="3.0.0",
    docs_url="/docs" if settings.ENVIRONMENT == "development" else None
)

# Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(LoggingMiddleware)

# Favicon handler
@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    return Response(status_code=204)

# Root route
@app.get("/", tags=["System"])
async def root():
    return {
        "message": f"Welcome to {settings.PROJECT_NAME}",
        "status": "online",
        "docs": "/docs" if settings.ENVIRONMENT == "development" else "Private"
    }

# Health Check
@app.get("/health", response_model=HealthResponse, tags=["System"])
async def health_check():
    return HealthResponse(status="healthy")

# Include Routes
app.include_router(chat.router)

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
