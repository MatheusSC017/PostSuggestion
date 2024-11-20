from unittest.mock import MagicMock

import pytest
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication

from ui.post import GeneratePostUI


@pytest.fixture
def qt_app():
    app = QApplication([])
    yield app
    app.quit()


@pytest.fixture
def fake_assistant():
    fake_client = MagicMock()
    fake_client.send_request.return_value = ["Suggestion 1", "Suggestion 2", "Suggestion 3"]
    return fake_client


@pytest.fixture
def generate_post_ui(qt_app, fake_assistant):
    return GeneratePostUI(suggestions=[], test_client=fake_assistant)


def test_initial_ui_state(generate_post_ui):
    assert generate_post_ui.emojis_cb.currentText() == "No"
    assert generate_post_ui.type_cb.currentText() == "Product"
    assert generate_post_ui.size_edit.text() == "500"
    assert generate_post_ui.language_cb.currentText() == "English"


# def test_post_generation(generate_post_ui, qtbot):
#     generate_post_ui.post_content_edit.setText("Original text to generate the post")
#     assert len(generate_post_ui.suggestions) == 0
#     qtbot.mouseClick(generate_post_ui.generate_posts_button, Qt.MouseButton.LeftButton)
#     qtbot.wait(1000)
#     assert len(generate_post_ui.suggestions) == 3
#
#     assert generate_post_ui.suggestions[0] == "Suggestion 1"
#     assert generate_post_ui.suggestions[1] == "Suggestion 2"
#     assert generate_post_ui.suggestions[2] == "Suggestion 3"
#
#     generate_post_ui.close()
#     del generate_post_ui
