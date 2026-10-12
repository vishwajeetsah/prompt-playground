"""Request/response schemas for the chat API."""

from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    prompt: str = Field(min_length=1, max_length=4000)
    system: str | None = Field(default=None, max_length=2000)


class ChatResponse(BaseModel):
    reply: str
    latency_s: float
    model: str
    mock_mode: bool


class HealthResponse(BaseModel):
    status: str
    mock_mode: bool
    model: str


class ModelInfo(BaseModel):
    id: str
    name: str
    description: str
