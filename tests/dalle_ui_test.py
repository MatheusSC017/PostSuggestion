import os
from unittest.mock import MagicMock, patch

import pytest
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QImage, QPixmap
from PyQt6.QtWidgets import QApplication, QFileDialog, QMessageBox

from ui.dalle import EditImageUI, GenerateImageUI, ImageVariationUI
from utils.validations import IMAGE_VALIDATIONS

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
    fake_client.generate_variations.return_value = (TEST_IMAGE_LINK, TEST_IMAGE_LINK)
    return fake_client


@pytest.fixture
def generate_image_ui(qt_app, fake_assistant):
    return GenerateImageUI(test_client=fake_assistant)


@pytest.fixture
def edit_image_ui(qt_app, fake_assistant):
    return EditImageUI(test_client=fake_assistant)


@pytest.fixture
def image_variation_ui(qt_app, fake_assistant):
    return ImageVariationUI(test_client=fake_assistant)


def test_initial_state_generate(generate_image_ui):
    assert generate_image_ui.prompt_image_edit.text() == ""
    assert generate_image_ui.size_combobox.currentText() == "Select"
    assert generate_image_ui.quality_combobox.currentText() == "Select"


def test_generate_image_parameter_error(generate_image_ui):
    parameters = {
        "Prompt": ("", "512x512", "standard"),
        "Size": ("Prompt text to generate image", "Select", "standard"),
        "Quality": ("Prompt text to generate image", "512x512", "Select"),
    }

    for parameter, inputs in parameters.items():
        with patch.object(QMessageBox, "exec", return_value=None) as mock_messagebox:
            with patch.object(QMessageBox, "setText") as mock_set_text:
                generate_image_ui.prompt_image_edit.setText(inputs[0])
                generate_image_ui.size_combobox.setCurrentText(inputs[1])
                generate_image_ui.quality_combobox.setCurrentText(inputs[2])

                generate_image_ui.generate_image_button.click()

                mock_set_text.assert_called_with(IMAGE_VALIDATIONS[parameter][1])

                mock_messagebox.reset_mock()
                mock_set_text.reset_mock()


def test_generate_image(generate_image_ui):
    generate_image_ui.prompt_image_edit.setText(
        "Create a image of a cat playing with a ball"
    )
    generate_image_ui.size_combobox.setCurrentText("512x512")
    generate_image_ui.quality_combobox.setCurrentText("standard")
    assert generate_image_ui.image is None
    generate_image_ui.generate_image_button.click()
    assert generate_image_ui.image is not None


def test_save_generated_image(generate_image_ui, tmp_path):
    test_image = QImage(100, 100, QImage.Format.Format_RGBA64)
    test_image.fill(Qt.GlobalColor.white)

    test_file_path = tmp_path / "saved_image"
    with patch.object(
        QFileDialog, "getSaveFileName", return_value=(str(test_file_path), None)
    ):
        generate_image_ui.image = test_image

        generate_image_ui.save_image_button.click()

        saved_image_path = f"{test_file_path}.png"
        assert os.path.exists(saved_image_path), "The image file was not saved"

        saved_image = QImage(saved_image_path)
        assert not saved_image.isNull(), "The saved image is invalid"
        assert (
            saved_image.size() == test_image.size()
        ), "The saved image size does not match"
        assert (
            saved_image.format() == test_image.format()
        ), "The saved image format does not match"


def test_initial_state_edit(edit_image_ui):
    assert edit_image_ui.prompt_image_edit.text() == ""
    assert edit_image_ui.size_combobox.currentText() == "Select"


def test_edit_image_parameter_error(edit_image_ui):
    test_image = QImage(100, 100, QImage.Format.Format_RGBA64)
    test_image.fill(Qt.GlobalColor.white)

    edit_image_ui.original_image = test_image
    edit_image_ui.mask = test_image.copy()

    parameters = {
        "Prompt": ("", "512x512"),
        "Size": ("Prompt text to generate image", "Select"),
    }

    for parameter, inputs in parameters.items():
        with patch.object(QMessageBox, "exec", return_value=None) as mock_messagebox:
            with patch.object(QMessageBox, "setText") as mock_set_text:
                edit_image_ui.prompt_image_edit.setText(inputs[0])
                edit_image_ui.size_combobox.setCurrentText(inputs[1])

                edit_image_ui.edit_image_button.click()

                mock_set_text.assert_called_with(IMAGE_VALIDATIONS[parameter][1])

                mock_messagebox.reset_mock()
                mock_set_text.reset_mock()


def test_edit_image(edit_image_ui):
    test_image = QImage(100, 100, QImage.Format.Format_RGBA64)
    test_image.fill(Qt.GlobalColor.white)

    edit_image_ui.original_image = test_image
    edit_image_ui.mask = test_image.copy()
    edit_image_ui.prompt_image_edit.setText("Delete the ball and include a mouse")
    edit_image_ui.size_combobox.setCurrentText("512x512")
    assert edit_image_ui.image is None
    edit_image_ui.edit_image_button.click()
    assert edit_image_ui.image is not None


def test_initial_state_variation(image_variation_ui):
    assert image_variation_ui.original_image is None
    assert image_variation_ui.variation_1_image is None
    assert image_variation_ui.variation_2_image is None
    assert image_variation_ui.original_pixmap is None
    assert image_variation_ui.variation_1_pixmap is None
    assert image_variation_ui.variation_2_pixmap is None


def test_generate_variations(image_variation_ui):
    test_image = QImage(100, 100, QImage.Format.Format_RGBA64)
    test_image.fill(Qt.GlobalColor.white)

    image_variation_ui.original_image = test_image
    image_variation_ui.original_pixmap = QPixmap.fromImage(test_image)

    image_variation_ui.generate_variation_button.click()
    assert image_variation_ui.variation_1_image is not None
    assert image_variation_ui.variation_2_image is not None
    assert image_variation_ui.variation_1_pixmap is not None
    assert image_variation_ui.variation_2_pixmap is not None
