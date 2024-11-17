import json

import pytest

from core.adjustment import AdjustmentPostAssitant
from tests.fake_openai import fake_openai_client
from utils.types import Configs


@pytest.fixture
def assistant(fake_openai_client):
    client = fake_openai_client(json.dumps({"post": "New adjustment"}))
    assistant = AdjustmentPostAssitant(
        post="Initial post that will be adjusted", test_client=client
    )
    return assistant


def test_initial_message(assistant):
    assert "You are a helpful assistant" in assistant.messages[0]["content"]


def test_send_request(assistant):
    adjustment = "Adjust the post"
    configs = {
        "size": 500,
        "emojis": "Medium",
        "language": "English",
        "type": "Product",
    }
    adjusted_post = assistant.send_request(adjustment, **configs)

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
    assert len(kwargs["messages"]) == 3

    assert adjusted_post == "New adjustment"

    _ = assistant.send_request(adjustment, **configs)
    _, kwargs = assistant.client.chat.completions.create.call_args
    assert len(kwargs["messages"]) == 5


def test_undo_and_redo(assistant):
    assistant.messages.extend(
        [
            {"role": "user", "content": "Post adjustment"},
            {"role": "assistant", "content": "Adjusted post"},
            {"role": "user", "content": "Post adjustment again"},
            {"role": "assistant", "content": "New adjusted post"},
        ]
    )
    assert len(assistant.messages) == 5

    assistant.redo()
    assert len(assistant.messages) == 5

    assistant.undo()
    assert len(assistant.messages) == 3

    assistant.undo()
    assert len(assistant.messages) == 1

    assistant.undo()
    assert len(assistant.messages) == 1

    assistant.redo()
    assert len(assistant.messages) == 3
