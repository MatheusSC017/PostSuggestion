import pytest

from core.adjustment import AdjustmentPostAssitantWithoutHistory
from tests.fake_openai import fake_openai_client
from utils.types import Configs


@pytest.fixture
def assistant(fake_openai_client):
    client = fake_openai_client("New adjustment")
    assistant = AdjustmentPostAssitantWithoutHistory(test_client=client)
    return assistant


def test_initial_message(assistant):
    assert "You are a helpful assistant" in assistant.messages[0]["content"]


def test_send_request(assistant):
    post = "Initial post that will be adjusted"
    adjustment = "Adjust the post"
    configs = {
        "size": 500,
        "emojis": "Medium",
        "language": "English",
        "type": "Product",
    }
    adjusted_post = assistant.send_request(
        message=post, adjustments=adjustment, **configs
    )

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

    _ = assistant.send_request(message=post, adjustments=adjustment, **configs)
    _, kwargs = assistant.client.chat.completions.create.call_args
    assert len(kwargs["messages"]) == 5
