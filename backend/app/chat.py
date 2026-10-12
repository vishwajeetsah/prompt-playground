"""Chat backends: a deterministic mock plus any OpenAI-compatible HTTP API."""

from __future__ import annotations

import json
import time
import urllib.request

from app.config import Settings


def mock_reply(prompt: str, system: str | None = None) -> tuple[str, float]:
    """Offline reply: reflects the prompt and suggests prompt-engineering ideas."""
    start = time.perf_counter()
    lines = [
        "Mock mode is ON — no API key, no cost, no network.",
        "",
        f"You sent ({len(prompt)} chars): {prompt[:160]!r}"
        + ("…" if len(prompt) > 160 else ""),
    ]
    if system:
        lines.append(f"System instruction received ({len(system)} chars).")
    lines += [
        "",
        "Try in the playground: ask the model to 'explain like I'm five', "
        "to 'give three alternatives', or to 'think step by step'.",
    ]
    return "\n".join(lines), time.perf_counter() - start


def openai_compatible_reply(
    prompt: str, settings: Settings, system: str | None = None
) -> tuple[str, float]:
    """Call an OpenAI-compatible ``/chat/completions`` endpoint (stdlib only)."""
    messages = []
    if system:
        messages.append({"role": "system", "content": system})
    messages.append({"role": "user", "content": prompt})
    body = json.dumps(
        {"model": settings.model, "messages": messages, "temperature": 0.7}
    ).encode("utf-8")
    request = urllib.request.Request(
        f"{settings.base_url.rstrip('/')}/chat/completions",
        data=body,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    if settings.api_key:
        request.add_header("Authorization", f"Bearer {settings.api_key}")
    start = time.perf_counter()
    try:
        with urllib.request.urlopen(request, timeout=120) as response:
            payload = json.loads(response.read().decode("utf-8"))
    except Exception as exc:
        raise RuntimeError(f"model request failed: {exc}") from exc
    latency = time.perf_counter() - start
    try:
        text = payload["choices"][0]["message"]["content"]
    except (KeyError, IndexError, TypeError) as exc:
        raise RuntimeError(f"unexpected API response shape: {payload!r}") from exc
    return text or "", latency


def generate_reply(
    prompt: str, settings: Settings, system: str | None = None
) -> tuple[str, float]:
    """Generate a reply using the mock or the configured real backend."""
    if settings.mock_mode:
        return mock_reply(prompt, system)
    return openai_compatible_reply(prompt, settings, system)
