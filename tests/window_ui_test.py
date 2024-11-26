import os.path
from unittest.mock import patch

import pytest
from PyQt6.QtWidgets import QApplication, QInputDialog

from ui.window import BASE_PATH, MainWindow


@pytest.fixture
def qt_app():
    app = QApplication([])
    yield app
    app.quit()


@pytest.fixture
def window_ui(qt_app):
    return MainWindow()


def test_save_suggestions(window_ui):
    test_file_path = f"{BASE_PATH}/files/suggestions.txt"
    with patch.object(QInputDialog, "exec"):
        with patch.object(QInputDialog, "textValue", return_value="suggestions"):
            assert window_ui.suggestions == []

            window_ui.save()

            assert os.path.exists(test_file_path)


def test_load_suggestions(window_ui):
    test_suggestions = ["Suggestion 1", "Suggestion 2", "Suggestion 3"]

    test_file_path = f"{BASE_PATH}/files/suggestions.txt"
    with open(test_file_path, "w") as file:
        for post in test_suggestions:
            file.write(f"{post}\n")

    with patch.object(QInputDialog, "exec"):
        with patch.object(QInputDialog, "textValue", return_value="suggestions"):
            assert window_ui.suggestions == []

            window_ui.load()

            assert window_ui.suggestions == test_suggestions
