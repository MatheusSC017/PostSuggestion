import io
from unittest.mock import MagicMock

import pytest
from PIL import Image

from core.images import Dalle
from tests.fake_openai import fake_openai_dalle_client


@pytest.fixture
def assistant(fake_openai_dalle_client):
    client = fake_openai_dalle_client()
    assistant_instance = Dalle(test_client=client)
    return assistant_instance


def test_generate_image(assistant):
    response = assistant.generate_image("Cat playing with a ball")
    assert response == "Generated image"


def test_edit_image(assistant):
    response = assistant.update_image(
        "Delete the person in the background",
        genenerate_image_bytes(),
        genenerate_image_bytes(),
    )
    assert response == "Generated image"


def test_generate_variations(assistant):
    response = assistant.generate_variations(
        "The cat is playing with other cats",
        genenerate_image_bytes(),
    )
    assert len(response) == 2
    assert response[0] == "Generated image"
    assert response[1] == "Generated image"


def genenerate_image_bytes():
    image = Image.new("RGB", (1024, 1024), color="white")

    image_bytes = io.BytesIO()
    image.save(image_bytes, format="PNG")
    image_bytes.seek(0)

    image_byte_data = image_bytes.getvalue()
    return image_byte_data
