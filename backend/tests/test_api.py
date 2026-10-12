"""API tests (run against the mock backend — no network needed)."""

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health():
    response = client.get("/api/health")
    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "ok"
    assert body["mock_mode"] is True


def test_models_lists_mock():
    response = client.get("/api/models")
    assert response.status_code == 200
    models = response.json()
    assert len(models) == 1
    assert models[0]["id"] == "mock-echo-v1"


def test_chat_returns_reply():
    response = client.post("/api/chat", json={"prompt": "Hello!"})
    assert response.status_code == 200
    body = response.json()
    assert "Mock mode" in body["reply"]
    assert body["latency_s"] >= 0
    assert body["mock_mode"] is True


def test_chat_with_system_prompt():
    response = client.post(
        "/api/chat", json={"prompt": "Hi", "system": "Be concise."}
    )
    assert response.status_code == 200
    assert "System instruction" in response.json()["reply"]


def test_chat_rejects_empty_prompt():
    response = client.post("/api/chat", json={"prompt": ""})
    assert response.status_code == 422
