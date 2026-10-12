"""Runtime configuration, read from environment variables."""

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Backend settings.

    Set ``MOCK_MODE=false`` and provide ``API_KEY`` to call a real
    OpenAI-compatible endpoint instead of the built-in mock.
    """

    mock_mode: bool = True
    model: str = "mock-echo-v1"
    base_url: str = "https://api.openai.com/v1"
    api_key: str | None = None
    cors_origins: list[str] = ["http://localhost:5173"]

    model_config = {"env_prefix": "PP_"}


settings = Settings()
