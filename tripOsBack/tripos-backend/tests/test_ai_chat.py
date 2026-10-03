import httpx
import pytest
from fastapi import HTTPException

from app.core.config import settings
from app.services.ai_service import AIService


def test_ai_chat_saves_user_and_assistant_messages(
    client,
    auth_headers,
    monkeypatch,
):
    user = client.get("/api/v1/users/me", headers=auth_headers)
    assert user.status_code == 200

    conversation = client.post(
        "/api/v1/ai/conversations",
        headers=auth_headers,
        json={
            "user_id": user.json()["id"],
            "title": "Japan itinerary",
        },
    )
    assert conversation.status_code == 201, conversation.text

    class FakeAIService:
        def generate_response(self, messages):
            assert messages[-1] == {
                "role": "user",
                "content": "Plan a weekend in Tokyo.",
            }
            assert messages[0]["role"] == "system"
            return "Here is a relaxed two-day Tokyo plan."

    monkeypatch.setattr(
        "app.controllers.ai.ai_message_controller.AIService",
        FakeAIService,
    )
    response = client.post(
        f"/api/v1/ai/conversations/{conversation.json()['id']}/messages",
        headers=auth_headers,
        json={"message": "Plan a weekend in Tokyo."},
    )

    assert response.status_code == 200, response.text
    payload = response.json()
    assert payload["user_message"]["role"] == "user"
    assert payload["user_message"]["message"] == "Plan a weekend in Tokyo."
    assert payload["assistant_message"]["role"] == "assistant"
    assert payload["assistant_message"]["message"] == (
        "Here is a relaxed two-day Tokyo plan."
    )
    stored_messages = client.get(
        "/api/v1/ai/messages",
        headers=auth_headers,
    )
    assert stored_messages.status_code == 200
    assert len(stored_messages.json()) == 2


def test_ai_service_uses_configured_provider_base_url(monkeypatch):
    monkeypatch.setattr(settings, "OPENAI_API_KEY", "test-key")
    monkeypatch.setattr(
        settings,
        "OPENAI_BASE_URL",
        "https://openrouter.ai/api/v1/",
    )
    response = httpx.Response(
        200,
        json={"choices": [{"message": {"content": "Hello back."}}]},
        request=httpx.Request(
            "POST",
            "https://openrouter.ai/api/v1/chat/completions",
        ),
    )
    requested = {}

    def fake_post(url, **kwargs):
        requested["url"] = url
        requested["kwargs"] = kwargs
        return response

    monkeypatch.setattr("app.services.ai_service.httpx.post", fake_post)

    result = AIService().generate_response([{"role": "user", "content": "Hello"}])

    assert result == "Hello back."
    assert requested["url"] == "https://openrouter.ai/api/v1/chat/completions"
    assert requested["kwargs"]["headers"]["Authorization"] == "Bearer test-key"


@pytest.mark.parametrize(
    ("status_code", "provider_error", "expected_detail"),
    [
        (401, "Invalid API key", "OPENAI_BASE_URL"),
        (429, "Quota exceeded", "quota and rate limits"),
        (400, "Unknown model", "Unknown model"),
    ],
)
def test_ai_service_explains_provider_errors(
    monkeypatch,
    status_code,
    provider_error,
    expected_detail,
):
    monkeypatch.setattr(settings, "OPENAI_API_KEY", "test-key")
    response = httpx.Response(
        status_code,
        json={"error": {"message": provider_error}},
        request=httpx.Request("POST", "https://api.openai.com/v1/chat/completions"),
    )
    monkeypatch.setattr(
        "app.services.ai_service.httpx.post",
        lambda *args, **kwargs: response,
    )

    with pytest.raises(HTTPException) as error:
        AIService().generate_response([{"role": "user", "content": "Hello"}])

    assert error.value.status_code == 502
    assert expected_detail in error.value.detail
