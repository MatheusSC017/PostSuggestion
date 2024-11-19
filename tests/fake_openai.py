import json
from unittest.mock import MagicMock

import pytest


@pytest.fixture
def fake_openai_chat_client():
    def _fake_openai_client(content):
        fake_client = MagicMock()
        fake_response = MagicMock()
        fake_response.model_dump_json.return_value = json.dumps(
            {"choices": [{"message": {"content": content}}]}
        )
        fake_client.chat.completions.create.return_value = fake_response
        return fake_client

    return _fake_openai_client


@pytest.fixture
def fake_openai_dalle_client():
    def _fake_openai_client():
        fake_client = MagicMock()
        fake_response = MagicMock()

        image_url = MagicMock()
        image_url.url = "Generated image"
        fake_response.data = [
            image_url,
        ]

        fake_client.images.generate.return_value = fake_response
        fake_client.images.edit.return_value = fake_response

        fake_response.data.append(image_url)

        fake_client.images.create_variation.return_value = fake_response

        return fake_client

    return _fake_openai_client
