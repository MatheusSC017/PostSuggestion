import pytest

from core.chat import Chat
from tests.fake_openai import fake_openai_chat_client


@pytest.fixture
def assistant(fake_openai_chat_client):
    client = fake_openai_chat_client("New message from the assistant")
    assistant_instance = Chat(test_client=client)
    return assistant_instance


def test_initial_message(assistant):
    assert "You are a helpful assistant" in assistant.messages[0]["content"]


def test_send_request(assistant):
    assert len(assistant.messages) == 1

    response = assistant.send_request("Question to the assistant")
    assert response == "New message from the assistant"

    assert len(assistant.messages) == 3
