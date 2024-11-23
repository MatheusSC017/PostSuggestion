from unittest.mock import MagicMock

import pytest
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QImage

from ui.dalle import GenerateImageUI, EditImageUI

TEST_IMAGE_LINK = "https://images.unsplash.com/photo-1720048169707-a32d6dfca0b3?q=80&w=1740&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDF8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D"


@pytest.fixture
def qt_app():
    app = QApplication([])
    yield app
    app.quit()


@pytest.fixture
def fake_assistant():
    fake_client = MagicMock()
    fake_client.generate_image.return_value = TEST_IMAGE_LINK
    fake_client.update_image.return_value = TEST_IMAGE_LINK
    return fake_client


@pytest.fixture
def generate_image_ui(qt_app, fake_assistant):
    return GenerateImageUI(test_client=fake_assistant)


@pytest.fixture
def edit_image_ui(qt_app, fake_assistant):
    return EditImageUI(test_client=fake_assistant)


def test_initial_state_generate(generate_image_ui):
    assert generate_image_ui.prompt_image_edit.text() == ""
    assert generate_image_ui.size_combobox.currentText() == "256x256"
    assert generate_image_ui.quality_combobox.currentText() == "standard"


def test_generate_image(generate_image_ui):
    generate_image_ui.prompt_image_edit.setText(
        "Create a image of a cat playing with a ball"
    )
    assert generate_image_ui.image is None
    generate_image_ui.generate_image_button.click()
    assert generate_image_ui.image is not None


def test_initial_state_edit(edit_image_ui):
    assert edit_image_ui.prompt_image_edit.text() == ""
    assert edit_image_ui.size_combobox.currentText() == "256x256"


def test_edit_image(edit_image_ui):
    test_image = QImage(100, 100, QImage.Format.Format_RGBA64)
    test_image.fill(Qt.GlobalColor.white)

    edit_image_ui.original_image = test_image
    edit_image_ui.mask = test_image.copy()
    edit_image_ui.prompt_image_edit.setText("Delete the ball and include a mouse")
    assert edit_image_ui.image is None
    edit_image_ui.edit_image_button.click()
    assert edit_image_ui.image is not None
