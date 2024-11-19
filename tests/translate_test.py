import pytest

from core.translator import TranslatorAssistant
from tests.fake_openai import fake_openai_chat_client


@pytest.fixture
def assistant(fake_openai_chat_client):
    client = fake_openai_chat_client("Translated post")
    assistant_instance = TranslatorAssistant(test_client=client)
    return assistant_instance


def test_initial_message(assistant):
    assert "You are a helpful assistant" in assistant.messages[0]["content"]


def test_set_language(assistant):
    assert assistant.language == "English"

    assistant.set_language("Spanish")

    assert assistant.language == "Spanish"


def test_send_request(assistant):
    translated_post = assistant.send_request("Input post")

    assistant.client.chat.completions.create.assert_called_once()
    _, kwargs = assistant.client.chat.completions.create.call_args
    assert kwargs["model"] == "gpt-3.5-turbo"
    assert "Language" in kwargs["messages"][-2]["content"]

    assert len(assistant.messages) == 3
    assert translated_post == "Translated post"
