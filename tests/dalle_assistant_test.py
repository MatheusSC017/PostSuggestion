from unittest.mock import MagicMock

import pytest

from core.images import Dalle
from tests.fake_openai import fake_openai_dalle_client
from utils.images import genenerate_image_bytes


@pytest.fixture
def assistant(fake_openai_dalle_client):
    client = fake_openai_dalle_client()
    assistant_instance = Dalle(test_client=client)
    return assistant_instance


def test_generate_image(assistant):
    assert isinstance(assistant.client, MagicMock)
    response = assistant.generate_image("Cat playing with a ball")
    assert response == "Generated image"


def test_edit_image(assistant):
    assert isinstance(assistant.client, MagicMock)
    response = assistant.update_image(
        "Delete the person in the background",
        genenerate_image_bytes(),
        genenerate_image_bytes(),
    )
    assert response == "Generated image"


def test_generate_variations(assistant):
    assert isinstance(assistant.client, MagicMock)
    response = assistant.generate_variations(genenerate_image_bytes())
    assert len(response) == 2
    assert response[0] == "Generated image"
    assert response[1] == "Generated image"
