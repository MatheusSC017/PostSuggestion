from unittest.mock import MagicMock
import json

import pytest

from core.post import PostSuggestAssistant
from tests.fake_openai import fake_openai_chat_client
from utils.types import Configs


@pytest.fixture
def assistant(fake_openai_chat_client):
    client = fake_openai_chat_client(
        json.dumps(
            {
                "posts": [
                    {"Post1": "Suggestion 1"},
                    {"Post2": "Suggestion 2"},
                    {"Post3": "Suggestion 3"},
                ]
            }
        )
    )
    assistant_instance = PostSuggestAssistant(test_client=client)
    return assistant_instance


def test_initial_state(assistant):
    assert isinstance(assistant.client, MagicMock)
    assert "You are a helpful assistant" in assistant.messages[0]["content"]


def test_send_request(assistant):
    message = "Create posts about technology trends"
    configs = {
        "size": 500,
        "emojis": "Medium",
        "language": "English",
        "type": "Product",
    }
    assert len(assistant.suggestions) == 0
    suggestions = assistant.send_request(message, **configs)
    assert len(assistant.suggestions) == 3

    assistant.client.chat.completions.create.assert_called_once()
    _, kwargs = assistant.client.chat.completions.create.call_args
    assert kwargs["model"] == "gpt-3.5-turbo"
    assert "Rules" in kwargs["messages"][-2]["content"]
    for config_key in configs.keys():
        assert (
            ": ".join(
                (
                    getattr(Configs, config_key.upper(), config_key),
                    str(configs[config_key]),
                )
            )
            in kwargs["messages"][-2]["content"]
        )

    assert len(suggestions) == 3
    assert suggestions == ["Suggestion 1", "Suggestion 2", "Suggestion 3"]
