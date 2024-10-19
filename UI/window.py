from functools import partial
from pathlib import Path

from dotenv import load_dotenv
from PyQt6.QtCore import pyqtSignal, pyqtSlot
from PyQt6.QtGui import QAction, QIntValidator
from PyQt6.QtWidgets import (
    QApplication,
    QComboBox,
    QHBoxLayout,
    QInputDialog,
    QLabel,
    QLineEdit,
    QMainWindow,
    QMenu,
    QMenuBar,
    QMessageBox,
    QPushButton,
    QScrollArea,
    QSizePolicy,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

from cli import OpenAIAssistants
from Core.adjustment import AdjustmentPostAssitantWithoutHistory
from Utils.types import Emojis

BASE_PATH = Path(__file__).resolve().parent.parent


class GeneratePostUI:
    def set_suggest_post_ui(self):
        main_layout = QHBoxLayout()

        input_layout = QVBoxLayout()

        column_options_1 = QVBoxLayout()
        column_options_1.addWidget(QLabel("Emojis"))
        self.emojis = QComboBox()
        self.emojis.addItems(["No", "Low", "Medium", "High"])
        column_options_1.addWidget(self.emojis)
        column_options_1.addWidget(QLabel("Type"))
        self.type = QComboBox()
        self.type.addItems(["Product", "Service", "Event", "Others"])
        column_options_1.addWidget(self.type)

        column_options_2 = QVBoxLayout()
        column_options_2.addWidget(QLabel("Size"))
        self.size = QLineEdit()
        self.size.setText("100")
        self.size.setValidator(QIntValidator(100, 5000))
        column_options_2.addWidget(self.size)
        column_options_2.addWidget(QLabel("Language"))
        self.language = QComboBox()
        self.language.addItems(["English", "Potuguese", "Spanish"])
        column_options_2.addWidget(self.language)

        options = QHBoxLayout()
        options.addLayout(column_options_1)
        options.addLayout(column_options_2)
        input_layout.addLayout(options)

        input_layout.addWidget(QLabel("Type your request:"))
        self.post_content = QTextEdit()
        self.post_content.setLineWrapMode(QTextEdit.LineWrapMode.WidgetWidth)
        input_layout.addWidget(self.post_content)

        self.generate_posts_button = QPushButton("Generate Posts")
        self.generate_posts_button.clicked.connect(self.generate_posts)
        form_options = QHBoxLayout()
        form_options.addStretch()
        form_options.addWidget(self.generate_posts_button)
        input_layout.addLayout(form_options)

        output_layout = QVBoxLayout()

        output_layout.addWidget(QLabel("Suggeestions"))
        self.generated_posts = QVBoxLayout()
        container = QWidget()
        container.setLayout(self.generated_posts)
        scroll_posts = QScrollArea()
        scroll_posts.setWidget(container)
        scroll_posts.setWidgetResizable(True)
        output_layout.addWidget(scroll_posts)

        for suggestion in self.assistants.post_assistant.suggestions:
            post = QLabel(suggestion)
            post.setWordWrap(True)
            post.setContentsMargins(5, 10, 5, 20)
            post_container = QHBoxLayout()
            post_container.addWidget(post)
            self.generated_posts.addLayout(post_container)

        main_layout.addLayout(input_layout)
        main_layout.addLayout(output_layout)

        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

    def generate_posts(self):
        self.generate_posts_button.setDisabled(True)
        emojis = str(self.emojis.currentText())
        post_type = str(self.type.currentText())
        language = str(self.language.currentText())
        size = int(self.size.text())
        post_content = self.post_content.toPlainText()

        if emojis not in ["No", "Low", "Medium", "High"]:
            dlg = QMessageBox(self)
            dlg.setWindowTitle("Error")
            dlg.setText(
                'The value for Emojis must be between ["No", "Low", "Medium", "High"]'
            )
            dlg.exec()
            return

        if post_type not in ["Product", "Service", "Event", "Others"]:
            dlg = QMessageBox(self)
            dlg.setWindowTitle("Error")
            dlg.setText(
                'The value for Emojis must be between ["Product", "Service", "Event", "Others"]'
            )
            dlg.exec()
            return

        if language not in ["English", "Potuguese", "Spanish"]:
            dlg = QMessageBox(self)
            dlg.setWindowTitle("Error")
            dlg.setText(
                'The value for Emojis must be between ["English", "Potuguese", "Spanish"]'
            )
            dlg.exec()
            return

        if 100 > size > 5000:
            dlg = QMessageBox(self)
            dlg.setWindowTitle("Error")
            dlg.setText("The generated post size must be between 100 and 5000")
            dlg.exec()
            return

        if len(post_content) <= 30:
            dlg = QMessageBox(self)
            dlg.setWindowTitle("Error")
            dlg.setText("Post content must be 30 characters or more")
            dlg.exec()
            return

        suggestions = self.assistants.get_suggestion(
            product_characteristics=post_content,
            Emojis=getattr(Emojis, emojis.upper()),
            Type=post_type,
            Language=language,
            Size=size,
        )
        for suggestion in suggestions:
            post = QLabel(suggestion)
            post.setWordWrap(True)
            post.setContentsMargins(5, 10, 5, 20)
            post_container = QHBoxLayout()
            post_container.addWidget(post)
            self.generated_posts.addLayout(post_container)
        self.generate_posts_button.setDisabled(False)


class ImprovePostUI:
    selected_post_index = None
    stored_posts = None

    def set_improve_post_ui(self):
        main_layout = QHBoxLayout()

        input_layout = QVBoxLayout()

        column_options_1 = QVBoxLayout()
        column_options_1.addWidget(QLabel("Emojis"))
        self.emojis = QComboBox()
        self.emojis.addItems(["No", "Low", "Medium", "High"])
        column_options_1.addWidget(self.emojis)
        column_options_1.addWidget(QLabel("Type"))
        self.type = QComboBox()
        self.type.addItems(["Product", "Service", "Event", "Others"])
        column_options_1.addWidget(self.type)

        column_options_2 = QVBoxLayout()
        column_options_2.addWidget(QLabel("Size"))
        self.size = QLineEdit()
        self.size.setText("100")
        self.size.setValidator(QIntValidator(100, 5000))
        column_options_2.addWidget(self.size)
        column_options_2.addWidget(QLabel("Language"))
        self.language = QComboBox()
        self.language.addItems(["English", "Potuguese", "Spanish"])
        column_options_2.addWidget(self.language)

        options = QHBoxLayout()
        options.addLayout(column_options_1)
        options.addLayout(column_options_2)
        input_layout.addLayout(options)

        original_post_layout = QHBoxLayout()
        original_post_layout.addWidget(QLabel("Post:"))
        original_post_layout.addStretch()
        select_post_button = QPushButton("Select Stored Posts")
        select_post_button.clicked.connect(self.open_stored_posts)
        original_post_layout.addWidget(select_post_button)
        input_layout.addLayout(original_post_layout)
        self.post_content = QTextEdit()
        self.post_content.setLineWrapMode(QTextEdit.LineWrapMode.WidgetWidth)
        input_layout.addWidget(self.post_content)

        input_layout.addWidget(QLabel("Type the improvements:"))
        self.post_improvements = QTextEdit()
        self.post_improvements.setLineWrapMode(QTextEdit.LineWrapMode.WidgetWidth)
        input_layout.addWidget(self.post_improvements)

        self.improve_post_button = QPushButton("Improve Post")
        self.improve_post_button.clicked.connect(self.improve_post)
        form_options = QHBoxLayout()
        form_options.addStretch()
        form_options.addWidget(self.improve_post_button)
        input_layout.addLayout(form_options)

        output_layout = QVBoxLayout()

        output_layout.addWidget(QLabel("History"))
        self.improved_posts = QVBoxLayout()
        container = QWidget()
        container.setLayout(self.improved_posts)
        scroll_posts = QScrollArea()
        scroll_posts.setWidget(container)
        scroll_posts.setWidgetResizable(True)
        output_layout.addWidget(scroll_posts)

        main_layout.addLayout(input_layout)
        main_layout.addLayout(output_layout)

        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

    def improve_post(self):
        self.improve_post_button.setDisabled(True)
        emojis = str(self.emojis.currentText())
        post_type = str(self.type.currentText())
        language = str(self.language.currentText())
        size = int(self.size.text())

        post_content = self.post_content.toPlainText()
        post_improvements = self.post_improvements.toPlainText()

        if emojis not in ["No", "Low", "Medium", "High"]:
            dlg = QMessageBox(self)
            dlg.setWindowTitle("Error")
            dlg.setText(
                'The value for Emojis must be between ["No", "Low", "Medium", "High"]'
            )
            dlg.exec()
            return

        if post_type not in ["Product", "Service", "Event", "Others"]:
            dlg = QMessageBox(self)
            dlg.setWindowTitle("Error")
            dlg.setText(
                'The value for Emojis must be between ["Product", "Service", "Event", "Others"]'
            )
            dlg.exec()
            return

        if language not in ["English", "Potuguese", "Spanish"]:
            dlg = QMessageBox(self)
            dlg.setWindowTitle("Error")
            dlg.setText(
                'The value for Emojis must be between ["English", "Potuguese", "Spanish"]'
            )
            dlg.exec()
            return

        if 100 > size > 5000:
            dlg = QMessageBox(self)
            dlg.setWindowTitle("Error")
            dlg.setText("The generated post size must be between 100 and 5000")
            dlg.exec()
            return

        if len(post_content) <= 30:
            dlg = QMessageBox(self)
            dlg.setWindowTitle("Error")
            dlg.setText("Post content must be 30 characters or more")
            dlg.exec()
            return

        if len(post_improvements) <= 30:
            dlg = QMessageBox(self)
            dlg.setWindowTitle("Error")
            dlg.setText("Post improvements must be 30 characters or more")
            dlg.exec()
            return

        if self.selected_post_index is None:
            suggestion = self.adjust_assistant.adjust_post(
                post_content,
                post_improvements,
                Emojis=getattr(Emojis, emojis.upper()),
                Type=post_type,
                Language=language,
                Size=size,
            )
        else:
            suggestion = self.assistants.adjustment(
                self.selected_post_index,
                post_improvements,
                Emojis=getattr(Emojis, emojis.upper()),
                Type=post_type,
                Language=language,
                Size=size,
            )

        post = QLabel(suggestion)
        post.setWordWrap(True)
        post.setContentsMargins(5, 10, 5, 20)
        post_container = QHBoxLayout()
        post_container.addWidget(post)
        self.improved_posts.addLayout(post_container)

        self.improve_post_button.setDisabled(False)

    def open_stored_posts(self):
        self.stored_posts = StoredPosts(self.assistants)
        self.stored_posts.selectPost.connect(self.set_selected_post)
        self.stored_posts.show()

    @pyqtSlot(str)
    def set_selected_post(self, post):
        self.selected_post_index = self.assistants.post_assistant.suggestions.index(
            post
        )
        self.post_content.setText(post)


class TranslatePostUI:
    stored_posts = None

    def set_translate_post_ui(self):
        main_layout = QHBoxLayout()

        input_layout = QVBoxLayout()

        original_post_layout = QHBoxLayout()
        original_post_layout.addWidget(QLabel("Post:"))
        original_post_layout.addStretch()
        select_post_button = QPushButton("Select Stored Posts")
        select_post_button.clicked.connect(self.open_stored_posts)
        original_post_layout.addWidget(select_post_button)
        input_layout.addLayout(original_post_layout)
        self.post_content = QTextEdit()
        self.post_content.setLineWrapMode(QTextEdit.LineWrapMode.WidgetWidth)
        input_layout.addWidget(self.post_content)

        self.translate_post_button = QPushButton("Translate Post")
        self.translate_post_button.clicked.connect(self.translate_post)
        form_options = QHBoxLayout()
        form_options.addStretch()
        form_options.addWidget(self.translate_post_button)
        input_layout.addLayout(form_options)

        output_layout = QVBoxLayout()

        output_layout.addWidget(QLabel("Translated post:"))
        self.post_translated = QTextEdit()
        self.post_translated.setEnabled(False)
        self.post_translated.setLineWrapMode(QTextEdit.LineWrapMode.WidgetWidth)
        output_layout.addWidget(self.post_translated)

        language_form = QHBoxLayout()
        language_form.addStretch()
        self.language = QComboBox()
        self.language.setMinimumWidth(200)
        self.language.addItems(["English", "Potuguese", "Spanish"])
        language_form.addWidget(self.language)
        output_layout.addLayout(language_form)

        main_layout.addLayout(input_layout)
        main_layout.addLayout(output_layout)

        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

    def translate_post(self):
        self.translate_post_button.setDisabled(True)

        post_content = self.post_content.toPlainText()

        if len(post_content) <= 30:
            dlg = QMessageBox(self)
            dlg.setWindowTitle("Error")
            dlg.setText("Post content must be 30 characters or more")
            dlg.exec()
            return

        self.assistants.translate_assistant.set_language(
            str(self.language.currentText())
        )
        translation = self.assistants.translate_message(post_content)
        self.post_translated.setText(translation)

        self.translate_post_button.setDisabled(False)

    @pyqtSlot(str)
    def selected_post(self, post):
        self.post_content.setText(post)

    def open_stored_posts(self):
        self.stored_posts = StoredPosts(self.assistants)
        self.stored_posts.selectPost.connect(self.selected_post)
        self.stored_posts.show()


class StoredPosts(QWidget):
    selectPost = pyqtSignal(str)

    def __init__(self, assistant):
        super().__init__()

        self.settings()
        self.init_ui(assistant)

    def settings(self):
        self.setWindowTitle("Stored Posts")
        self.setMinimumWidth(500)
        self.setMinimumHeight(700)

    def init_ui(self, assistant):
        main_layout = QVBoxLayout()

        generated_posts = QVBoxLayout()
        for post in assistant.post_assistant.suggestions:
            post_widget = QLabel(post)
            post_widget.setWordWrap(True)
            post_widget.setContentsMargins(5, 10, 5, 20)
            post_container = QHBoxLayout()
            post_container.addWidget(post_widget)
            post_button = QPushButton()
            post_button.setLayout(post_container)
            post_button.setSizePolicy(
                post_button.sizePolicy().horizontalPolicy(),
                QSizePolicy.Policy.Expanding,
            )
            post_button.adjustSize()
            post_button.clicked.connect(partial(self.select_post, post))
            generated_posts.addWidget(post_button)

        container = QWidget()
        container.setLayout(generated_posts)
        scroll_posts = QScrollArea()
        scroll_posts.setWidget(container)
        scroll_posts.setWidgetResizable(True)
        main_layout.addWidget(scroll_posts)

        self.setLayout(main_layout)

    @pyqtSlot(str)
    def select_post(self, post):
        self.selectPost.emit(post)
        self.close()


class MainWindow(QMainWindow, GeneratePostUI, ImprovePostUI, TranslatePostUI):

    def __init__(self):
        super().__init__()
        load_dotenv()
        self.assistants = OpenAIAssistants()
        self.adjust_assistant = AdjustmentPostAssitantWithoutHistory()

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

        file = QMenu("File", self)
        self.save_history = QAction("Save")
        self.save_history.triggered.connect(self.save)
        file.addAction(self.save_history)
        self.load_history = QAction("Load")
        self.load_history.triggered.connect(self.load)
        file.addAction(self.load_history)

        menu_bar.addMenu(post_assistants)
        menu_bar.addMenu(file)

    def save(self):
        file_name = QInputDialog(self)
        file_name.setWindowTitle("Save History")
        file_name.setLabelText("Enter the file name")
        if file_name.exec():
            with open(f"{BASE_PATH}/Files/{file_name.textValue()}.txt", "w") as file:
                for post in self.assistants.post_assistant.suggestions:
                    file.write(f"{post}\n")

    def load(self):
        file_name = QInputDialog(self)
        file_name.setWindowTitle("Load History")
        file_name.setLabelText("Enter the file name")
        if file_name.exec():
            with open(f"{BASE_PATH}/Files/{file_name.textValue()}.txt", "r") as file:
                for post in file:
                    self.assistants.post_assistant.suggestions.append(post)
