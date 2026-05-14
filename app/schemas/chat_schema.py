from pydantic import BaseModel, Field

class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1, max_length=4000)
    provider: str = Field(default="groq", description="Provider: gemini, groq, or llama")

class ChatResponse(BaseModel):
    success: bool
    provider: str
    reply: str

class HealthResponse(BaseModel):
    status: str
