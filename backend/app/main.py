"""FastAPI application: the Prompt Playground backend."""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from app import chat
from app.config import settings
from app.schemas import ChatRequest, ChatResponse, HealthResponse, ModelInfo

app = FastAPI(title="Prompt Playground API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/health", response_model=HealthResponse)
def health() -> HealthResponse:
    return HealthResponse(status="ok", mock_mode=settings.mock_mode, model=settings.model)


@app.get("/api/models", response_model=list[ModelInfo])
def list_models() -> list[ModelInfo]:
    if settings.mock_mode:
        return [
            ModelInfo(
                id="mock-echo-v1",
                name="Mock Echo v1",
                description="Deterministic offline mock. No API key needed.",
            )
        ]
    return [
        ModelInfo(
            id=settings.model,
            name=settings.model,
            description=f"OpenAI-compatible endpoint at {settings.base_url}",
        )
    ]


@app.post("/api/chat", response_model=ChatResponse)
def chat_endpoint(request: ChatRequest) -> ChatResponse:
    try:
        text, latency = chat.generate_reply(request.prompt, settings, request.system)
    except RuntimeError as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc
    return ChatResponse(
        reply=text,
        latency_s=latency,
        model=settings.model,
        mock_mode=settings.mock_mode,
    )
