from functools import partial
from pathlib import Path

from PyQt6.QtCore import pyqtSignal, pyqtSlot
from PyQt6.QtGui import QIntValidator
from PyQt6.QtWidgets import (QComboBox, QHBoxLayout, QLabel, QLineEdit,
                             QPushButton, QScrollArea, QSizePolicy, QTextEdit,
                             QVBoxLayout, QWidget)

from Core.adjustment import (AdjustmentPostAssitant,
                             AdjustmentPostAssitantWithoutHistory)
from Core.base import ErrorHandling
from Core.post import PostSuggestAssistant
from Core.translator import TranslatorAssistant
from Utils.types import Emojis

BASE_PATH = Path(__file__).resolve().parent.parent

VALIDATIONS = {
    "Emojis": (
        lambda emojis: emojis not in ["No", "Low", "Medium", "High"],
        'The value for Emojis must be between ["No", "Low", "Medium", "High"]',
    ),
    "Type": (
        lambda post_type: post_type not in ["Product", "Service", "Event", "Others"],
        'The value for Emojis must be between ["Product", "Service", "Event", "Others"]',
    ),
    "Language": (
        lambda language: language not in ["English", "Potuguese", "Spanish"],
        'The value for Emojis must be between ["English", "Potuguese", "Spanish"]',
    ),
    "Size": (
        lambda size: 100 > size > 5000,
        "The generated post size must be between 100 and 5000",
    ),
    "Content": (
        lambda post_content: len(post_content) <= 30,
        "Post content/improvements must be 30 characters or more",
    ),
}


class GeneratePostUI(QWidget, ErrorHandling):
    suggestions = []
    post_suggest_assistant = PostSuggestAssistant()

    def __init__(self, suggestions):
        super().__init__()
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

        for suggestion in self.suggestions:
            post = QLabel(suggestion)
            post.setWordWrap(True)
            post.setContentsMargins(5, 10, 5, 20)
            post_container = QHBoxLayout()
            post_container.addWidget(post)
            self.generated_posts.addLayout(post_container)

        main_layout.addLayout(input_layout)
        main_layout.addLayout(output_layout)

        self.setLayout(main_layout)

        self.suggestions = suggestions

    def generate_posts(self):
        self.generate_posts_button.setDisabled(True)
        emojis = str(self.emojis.currentText())
        post_type = str(self.type.currentText())
        language = str(self.language.currentText())
        size = int(self.size.text())
        post_content = self.post_content.toPlainText()

        for field, value in zip(
            ["Emojis", "Type", "Language", "Size", "Content"],
            [emojis, post_type, language, size, post_content],
        ):
            if field in VALIDATIONS and VALIDATIONS[field][0](value):
                self.error_handling(VALIDATIONS[field][1])
                return

        new_suggestions = self.post_suggest_assistant.get_suggestions(
            product_characteristics=post_content,
            Emojis=getattr(Emojis, emojis.upper()),
            Type=post_type,
            Language=language,
            Size=size,
        )

        self.suggestions.clear()
        self.suggestions.extend(new_suggestions)

        for suggestion in self.suggestions:
            post = QLabel(suggestion)
            post.setWordWrap(True)
            post.setContentsMargins(5, 10, 5, 20)
            post_container = QHBoxLayout()
            post_container.addWidget(post)
            self.generated_posts.addLayout(post_container)
        self.generate_posts_button.setDisabled(False)


class ImprovePostUI(QWidget, ErrorHandling):
    adjustment_posts = {}
    general_adjust_assistant = AdjustmentPostAssitantWithoutHistory()
    suggestions = []
    selected_post_index = None
    stored_posts = None

    def __init__(self, suggestions):
        super().__init__()
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

        self.setLayout(main_layout)

        self.suggestions = suggestions

    def improve_post(self):
        self.improve_post_button.setDisabled(True)
        emojis = str(self.emojis.currentText())
        post_type = str(self.type.currentText())
        language = str(self.language.currentText())
        size = int(self.size.text())

        post_content = self.post_content.toPlainText()
        post_improvements = self.post_improvements.toPlainText()

        for field, value in zip(
            ["Emojis", "Type", "Language", "Size", "Content", "Content"],
            [emojis, post_type, language, size, post_content, post_improvements],
        ):
            if field in VALIDATIONS and VALIDATIONS[field][0](value):
                self.error_handling(VALIDATIONS[field][1])
                return

        if self.selected_post_index is None:
            suggestion = self.general_adjust_assistant.adjust_post(
                post_content,
                post_improvements,
                Emojis=getattr(Emojis, emojis.upper()),
                Type=post_type,
                Language=language,
                Size=size,
            )
        else:
            suggestion = self.adjustment(
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

    def adjustment(self, post, adjustment_characteristics, **kwargs):
        if post not in self.adjustment_posts.keys():
            self.new_adjustment(post, **kwargs)

        return self.adjustment_posts[post].send_request(
            adjustment_characteristics, **kwargs
        )

    def new_adjustment(self, post, **kwargs):
        basic_configs = {}
        for key, value in kwargs.items():
            basic_configs[key] = value

        self.adjustment_posts[post] = AdjustmentPostAssitant(
            post=self.suggestions[post],
            basic_configs=basic_configs,
        )

    def end_adjustment(self, post):
        if post in self.adjustment_posts.keys():
            post_suggestion = self.adjustment_posts[post].messages[-1]["content"]
            del self.adjustment_posts[post]
            return post_suggestion
        raise Exception("Post not found")

    def open_stored_posts(self):
        self.stored_posts = StoredPosts(self.suggestions)
        self.stored_posts.selectPost.connect(self.set_selected_post)
        self.stored_posts.show()

    def set_selected_post(self, post):
        self.selected_post_index = self.suggestions.index(post)
        self.post_content.setText(post)


class TranslatePostUI(QWidget, ErrorHandling):
    translate_assistant = TranslatorAssistant()
    suggestions = []
    stored_posts = None

    def __init__(self, suggestions):
        super().__init__()
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

        self.setLayout(main_layout)

        self.suggestions = suggestions

    def translate_post(self):
        self.translate_post_button.setDisabled(True)

        post_content = self.post_content.toPlainText()
        language = str(self.language.currentText())

        for field, value in zip(["Language", "Content"], [language, post_content]):
            if field in VALIDATIONS and VALIDATIONS[field][0](value):
                self.error_handling(VALIDATIONS[field][1])
                return

        self.translate_assistant.set_language(language)
        translation = self.translate_message(post_content)
        self.post_translated.setText(translation)

        self.translate_post_button.setDisabled(False)

    @pyqtSlot(str)
    def selected_post(self, post):
        self.post_content.setText(post)

    def open_stored_posts(self):
        self.stored_posts = StoredPosts(self.suggestions)
        self.stored_posts.selectPost.connect(self.selected_post)
        self.stored_posts.show()

    def translate_message(self, message):
        return self.translate_assistant.send_request(message)


class StoredPosts(QWidget):
    selectPost = pyqtSignal(str)

    def __init__(self, suggestions):
        super().__init__()

        self.settings()
        self.init_ui(suggestions)

    def settings(self):
        self.setWindowTitle("Stored Posts")
        self.setMinimumWidth(500)
        self.setMinimumHeight(700)

    def init_ui(self, suggestions):
        main_layout = QVBoxLayout()

        generated_posts = QVBoxLayout()
        for post in suggestions:
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
