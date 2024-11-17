import json
from unittest.mock import MagicMock

import pytest


@pytest.fixture
def fake_openai_client():
    def _fake_openai_client(content):
        fake_client = MagicMock()
        fake_response = MagicMock()
        fake_response.model_dump_json.return_value = json.dumps(
            {"choices": [{"message": {"content": content}}]}
        )
        fake_client.chat.completions.create.return_value = fake_response
        return fake_client

    return _fake_openai_client
