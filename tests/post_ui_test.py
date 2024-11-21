from unittest.mock import MagicMock

import pytest
from PyQt6.QtWidgets import QApplication

from ui.post import GeneratePostUI


@pytest.fixture
def qt_app():
    app = QApplication([])
    yield app
    app.quit()


@pytest.fixture
def fake_assistant():
    def _fake_assistant(content):
        fake_client = MagicMock()
        fake_client.send_request.return_value = content
        return fake_client

    return _fake_assistant


@pytest.fixture
def generate_post_ui(qt_app, fake_assistant):
    assistant_instance = fake_assistant(
        [
            "Suggestion 1",
            "Suggestion 2",
            "Suggestion 3",
        ]
    )
    return GeneratePostUI(suggestions=[], test_client=assistant_instance)


def test_initial_ui_state(generate_post_ui):
    assert generate_post_ui.emojis_cb.currentText() == "No"
    assert generate_post_ui.type_cb.currentText() == "Product"
    assert generate_post_ui.size_edit.text() == "500"
    assert generate_post_ui.language_cb.currentText() == "English"


def test_post_generation(generate_post_ui):
    generate_post_ui.show()
    generate_post_ui.post_content_edit.setText("Original text to generate the post")
    assert len(generate_post_ui.suggestions) == 0
    generate_post_ui.generate_posts_button.click()
    assert len(generate_post_ui.suggestions) == 3

    assert generate_post_ui.suggestions[0] == "Suggestion 1"
    assert generate_post_ui.suggestions[1] == "Suggestion 2"
    assert generate_post_ui.suggestions[2] == "Suggestion 3"
