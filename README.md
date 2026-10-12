# Prompt Playground

A bilingual starter project — **Python (FastAPI) backend** + **TypeScript (React) frontend** — for experimenting with prompts against any OpenAI-compatible language model. Runs fully offline in mock mode: no API key, no cost.

> Built as a learning project: one repo, two languages, talking to each other over a typed HTTP API.

## Architecture

```
┌─────────────────────┐        ┌──────────────────────┐
│  frontend/          │  HTTP  │  backend/            │
│  TypeScript + React │ ─────▶ │  Python + FastAPI    │
│  chat UI            │  /api/*│  /api/chat            │
└─────────────────────┘        │  /api/models         │
                               │  /api/health         │
                               └──────────────────────┘
```

## Quickstart

**Backend** (Python 3.10+):

```bash
cd backend
pip install -e ".[test]"
uvicorn app.main:app --reload        # http://localhost:8000
```

**Frontend** (Node 18+):

```bash
cd frontend
npm install
npm run dev                         # http://localhost:5173
```

Or everything with Docker:

```bash
docker compose up --build
```

## Using a real model

```bash
cd backend
PP_MOCK_MODE=false PP_API_KEY="sk-..." PP_MODEL="gpt-4o-mini" \
  uvicorn app.main:app --reload
```

Any OpenAI-compatible endpoint works — set `PP_BASE_URL` (e.g. `http://localhost:11434/v1` for Ollama).

## API

| Method | Path          | Description                        |
| ------ | ------------- | ---------------------------------- |
| GET    | `/api/health` | Status, mock mode, active model    |
| GET    | `/api/models` | Available models                   |
| POST   | `/api/chat`   | `{"prompt": "...", "system": "…"}` → reply + latency |

## Project structure

```
backend/                 # Python: FastAPI API
  app/                   # main.py, chat.py, schemas.py, config.py
  tests/                 # pytest suite (mock-based, offline)
  Dockerfile
frontend/                # TypeScript: React + Vite chat UI
  src/                   # App.tsx, api.ts (typed client), styles.css
  Dockerfile
docker-compose.yml
.github/workflows/ci.yml # backend tests + frontend build
```

## Tests

```bash
cd backend && pytest -q
cd frontend && npm run build   # type-check + production build
```

## Ideas to extend

- [ ] Conversation history + multi-turn context
- [ ] Prompt templates library (few-shot, chain-of-thought presets)
- [ ] Side-by-side model comparison view
- [ ] Token usage and cost tracking per request
- [ ] Streaming responses (SSE) instead of waiting for full replies
- [ ] Save/share interesting prompt runs

## License

MIT — see [LICENSE](LICENSE).
