import pytest
import json
from unittest.mock import MagicMock
from core.post import PostSuggestAssistant


@pytest.fixture
def fake_openai_client():
    fake_client = MagicMock()
    fake_response = MagicMock()
    fake_response.model_dump_json.return_value = json.dumps(
        {
            "choices": [
                {
                    "message": {
                        "content": json.dumps(
                            {
                                "posts": [
                                    {"Post1": "Suggestion 1"},
                                    {"Post2": "Suggestion 2"},
                                    {"Post3": "Suggestion 3"},
                                ]
                            }
                        )
                    }
                }
            ]
        }
    )
    fake_client.chat.completions.create.return_value = fake_response
    return fake_client


@pytest.fixture
def assistant(fake_openai_client):
    assistant = PostSuggestAssistant(test_client=fake_openai_client)
    assistant.model = "gpt-3.5-turbo"
    assistant.basic_configs = {
        "size": "Medium",
        "language": "English",
        "emojis_allowed": 3,
    }
    return assistant


def test_initial_message(assistant):
    assert "You are a helpful assistant" in assistant.messages[0]["content"]


def test_send_request(assistant):
    message = "Create posts about technology trends"
    suggestions = assistant.send_request(message, size="Small", emojis_allowed=1)

    assistant.client.chat.completions.create.assert_called_once()
    _, kwargs = assistant.client.chat.completions.create.call_args
    assert kwargs["model"] == "gpt-3.5-turbo"
    assert "Rules" in kwargs["messages"][-2]["content"]

    assert len(suggestions) == 3
    assert suggestions == ["Suggestion 1", "Suggestion 2", "Suggestion 3"]
