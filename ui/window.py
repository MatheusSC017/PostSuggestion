from pathlib import Path

from dotenv import load_dotenv
from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import QInputDialog, QMainWindow, QMenu, QMenuBar

from ui.dalle import EditImageUI, GenerateImageUI, ImageVariationUI
from ui.post import GeneratePostUI, ImprovePostUI, TranslatePostUI

BASE_PATH = Path(__file__).resolve().parent.parent


class MainWindow(QMainWindow):
    suggestions = []
    main_window = None

    def __init__(self):
        super().__init__()
        load_dotenv()

        self.settings()
        self.init_ui()

    def settings(self):
        self.setWindowTitle("AI Assitants")
        self.setMinimumWidth(1000)
        self.setMinimumHeight(700)

    def init_ui(self):
        self.set_menu()

    def set_menu(self):
        menu_bar = QMenuBar(self)
        self.setMenuBar(menu_bar)

        post_assistants = QMenu("Posts", self)

        self.suggest_post_menu = QAction("Suggestion")
        self.suggest_post_menu.triggered.connect(self.set_suggest_post_ui)
        post_assistants.addAction(self.suggest_post_menu)
        self.improve_post_menu = QAction("Improvement")
        self.improve_post_menu.triggered.connect(self.set_improve_post_ui)
        post_assistants.addAction(self.improve_post_menu)
        self.translate_post_menu = QAction("Translate")
        self.translate_post_menu.triggered.connect(self.set_translate_post_ui)
        post_assistants.addAction(self.translate_post_menu)
        self.save_history = QAction("Save History")
        self.save_history.triggered.connect(self.save)
        post_assistants.addAction(self.save_history)
        self.load_history = QAction("Load History")
        self.load_history.triggered.connect(self.load)
        post_assistants.addAction(self.load_history)

        dalle_assistants = QMenu("Images", self)
        self.generate_image_menu = QAction("Create")
        self.generate_image_menu.triggered.connect(self.set_generate_image_ui)
        dalle_assistants.addAction(self.generate_image_menu)
        self.edit_image_menu = QAction("Edit")
        self.edit_image_menu.triggered.connect(self.set_image_edit_ui)
        dalle_assistants.addAction(self.edit_image_menu)
        self.image_variation_menu = QAction("Variations")
        self.image_variation_menu.triggered.connect(self.set_image_variation_ui)
        dalle_assistants.addAction(self.image_variation_menu)

        menu_bar.addMenu(post_assistants)
        menu_bar.addMenu(dalle_assistants)

    def set_suggest_post_ui(self):
        self.main_window = GeneratePostUI(self.suggestions)
        self.setCentralWidget(self.main_window)

    def set_improve_post_ui(self):
        self.main_window = ImprovePostUI(self.suggestions)
        self.setCentralWidget(self.main_window)

    def set_translate_post_ui(self):
        self.main_window = TranslatePostUI(self.suggestions)
        self.setCentralWidget(self.main_window)

    def set_generate_image_ui(self):
        self.main_window = GenerateImageUI()
        self.setCentralWidget(self.main_window)

    def set_image_edit_ui(self):
        self.main_window = EditImageUI()
        self.setCentralWidget(self.main_window)

    def set_image_variation_ui(self):
        self.main_window = ImageVariationUI()
        self.setCentralWidget(self.main_window)

    def save(self):
        file_name = QInputDialog(self)
        file_name.setWindowTitle("Save History")
        file_name.setLabelText("Enter the file name")
        if file_name.exec():
            with open(f"{BASE_PATH}/files/{file_name.textValue()}.txt", "w") as file:
                for post in self.suggestions:
                    file.write(f"{post}\n")

    def load(self):
        file_name = QInputDialog(self)
        file_name.setWindowTitle("Load History")
        file_name.setLabelText("Enter the file name")
        if file_name.exec():
            with open(f"{BASE_PATH}/files/{file_name.textValue()}.txt", "r") as file:
                for post in file:
                    self.suggestions.append(post.strip())
