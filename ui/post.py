from functools import partial
from pathlib import Path

from PyQt6.QtCore import Qt, pyqtSignal, pyqtSlot
from PyQt6.QtGui import QIntValidator
from PyQt6.QtWidgets import (QComboBox, QHBoxLayout, QLabel, QLineEdit,
                             QPushButton, QScrollArea, QSizePolicy, QTextEdit,
                             QVBoxLayout, QWidget)

from core.adjustment import (AdjustmentPostAssitant,
                             AdjustmentPostAssitantWithoutHistory)
from core.post import PostSuggestAssistant
from core.translator import TranslatorAssistant
from ui.base import ErrorHandling
from utils.types import Emojis
from utils.validations import POST_VALIDATIONS

BASE_PATH = Path(__file__).resolve().parent.parent


class GeneratePostUI(QWidget, ErrorHandling):
    suggestions = []
    post_suggest_assistant = PostSuggestAssistant()

    def __init__(self, suggestions):
        super().__init__()
        main_layout = QHBoxLayout()

        input_layout = QVBoxLayout()

        column_options_1_layout = QVBoxLayout()
        column_options_1_layout.addWidget(QLabel("Emojis"))
        self.emojis_cb = QComboBox()
        self.emojis_cb.addItems(["No", "Low", "Medium", "High"])
        column_options_1_layout.addWidget(self.emojis_cb)
        column_options_1_layout.addWidget(QLabel("Type"))
        self.type_cb = QComboBox()
        self.type_cb.addItems(["Product", "Service", "Event", "Others"])
        column_options_1_layout.addWidget(self.type_cb)

        column_options_2_layout = QVBoxLayout()
        column_options_2_layout.addWidget(QLabel("Size"))
        self.size_edit = QLineEdit()
        self.size_edit.setText("500")
        self.size_edit.setValidator(QIntValidator(100, 5000))
        column_options_2_layout.addWidget(self.size_edit)
        column_options_2_layout.addWidget(QLabel("Language"))
        self.language_cb = QComboBox()
        self.language_cb.addItems(["English", "Potuguese", "Spanish"])
        column_options_2_layout.addWidget(self.language_cb)

        options_layout = QHBoxLayout()
        options_layout.addLayout(column_options_1_layout)
        options_layout.addLayout(column_options_2_layout)
        input_layout.addLayout(options_layout)

        input_layout.addWidget(QLabel("Type your request:"))
        self.post_content_edit = QTextEdit()
        self.post_content_edit.setLineWrapMode(QTextEdit.LineWrapMode.WidgetWidth)
        input_layout.addWidget(self.post_content_edit)

        self.generate_posts_button = QPushButton("Generate Posts")
        self.generate_posts_button.clicked.connect(self.generate_posts)
        form_options_layout = QHBoxLayout()
        form_options_layout.addStretch()
        form_options_layout.addWidget(self.generate_posts_button)
        input_layout.addLayout(form_options_layout)

        output_layout = QVBoxLayout()

        output_layout.addWidget(QLabel("Suggeestions"))
        self.generated_posts_layout = QVBoxLayout()
        container = QWidget()
        container.setLayout(self.generated_posts_layout)
        posts_scroll = QScrollArea()
        posts_scroll.setWidget(container)
        posts_scroll.setWidgetResizable(True)
        output_layout.addWidget(posts_scroll)

        self.set_suggested_posts_labels()

        main_layout.addLayout(input_layout)
        main_layout.addLayout(output_layout)

        self.setLayout(main_layout)

        self.suggestions = suggestions

    def generate_posts(self):
        self.generate_posts_button.setDisabled(True)
        emojis = str(self.emojis_cb.currentText())
        post_type = str(self.type_cb.currentText())
        language = str(self.language_cb.currentText())
        size = int(self.size_edit.text())
        post_content = self.post_content_edit.toPlainText()

        for field, value in zip(
            ["Emojis", "Type", "Language", "Size", "Content"],
            [emojis, post_type, language, size, post_content],
        ):
            if field in POST_VALIDATIONS and POST_VALIDATIONS[field][0](value):
                self.error_handling(POST_VALIDATIONS[field][1])
                return

        new_suggestions = self.post_suggest_assistant.send_request(
            message=post_content,
            Emojis=getattr(Emojis, emojis.upper()),
            Type=post_type,
            Language=language,
            Size=size,
        )

        self.suggestions.clear()
        self.suggestions.extend(new_suggestions)

        self.set_suggested_posts_labels()
        self.generate_posts_button.setDisabled(False)

    def set_suggested_posts_labels(self):
        clear_layout(self.generated_posts_layout)
        for suggestion in self.suggestions:
            post = QLabel(suggestion)
            post.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
            post.setWordWrap(True)
            post.setContentsMargins(5, 10, 5, 20)
            post_container = QHBoxLayout()
            post_container.addWidget(post)
            self.generated_posts_layout.addLayout(post_container)


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

        column_options_1_layout = QVBoxLayout()
        column_options_1_layout.addWidget(QLabel("Emojis"))
        self.emojis_cb = QComboBox()
        self.emojis_cb.addItems(["No", "Low", "Medium", "High"])
        column_options_1_layout.addWidget(self.emojis_cb)
        column_options_1_layout.addWidget(QLabel("Type"))
        self.type_cb = QComboBox()
        self.type_cb.addItems(["Product", "Service", "Event", "Others"])
        column_options_1_layout.addWidget(self.type_cb)

        column_options_2_layout = QVBoxLayout()
        column_options_2_layout.addWidget(QLabel("Size"))
        self.size_edit = QLineEdit()
        self.size_edit.setText("100")
        self.size_edit.setValidator(QIntValidator(100, 5000))
        column_options_2_layout.addWidget(self.size_edit)
        column_options_2_layout.addWidget(QLabel("Language"))
        self.language_cb = QComboBox()
        self.language_cb.addItems(["English", "Potuguese", "Spanish"])
        column_options_2_layout.addWidget(self.language_cb)

        options = QHBoxLayout()
        options.addLayout(column_options_1_layout)
        options.addLayout(column_options_2_layout)
        input_layout.addLayout(options)

        original_post_layout = QHBoxLayout()
        original_post_layout.addWidget(QLabel("Post:"))
        original_post_layout.addStretch()
        select_post_button = QPushButton("Select Stored Posts")
        select_post_button.clicked.connect(self.open_stored_posts)
        original_post_layout.addWidget(select_post_button)
        input_layout.addLayout(original_post_layout)
        self.post_content_edit = QTextEdit()
        self.post_content_edit.setLineWrapMode(QTextEdit.LineWrapMode.WidgetWidth)
        input_layout.addWidget(self.post_content_edit)

        input_layout.addWidget(QLabel("Type the improvements:"))
        self.post_improvements_edit = QTextEdit()
        self.post_improvements_edit.setLineWrapMode(QTextEdit.LineWrapMode.WidgetWidth)
        input_layout.addWidget(self.post_improvements_edit)

        self.improve_post_button = QPushButton("Improve Post")
        self.improve_post_button.clicked.connect(self.improve_post)
        form_options_layout = QHBoxLayout()
        form_options_layout.addStretch()
        form_options_layout.addWidget(self.improve_post_button)
        input_layout.addLayout(form_options_layout)

        output_layout = QVBoxLayout()

        output_layout.addWidget(QLabel("History"))
        self.improved_posts_layout = QVBoxLayout()
        container = QWidget()
        container.setLayout(self.improved_posts_layout)
        posts_scroll = QScrollArea()
        posts_scroll.setWidget(container)
        posts_scroll.setWidgetResizable(True)
        output_layout.addWidget(posts_scroll)

        main_layout.addLayout(input_layout)
        main_layout.addLayout(output_layout)

        self.setLayout(main_layout)

        self.suggestions = suggestions

    def improve_post(self):
        self.improve_post_button.setDisabled(True)
        emojis = str(self.emojis_cb.currentText())
        post_type = str(self.type_cb.currentText())
        language = str(self.language_cb.currentText())
        size = int(self.size_edit.text())

        post_content = self.post_content_edit.toPlainText()
        post_improvements = self.post_improvements_edit.toPlainText()

        for field, value in zip(
            ["Emojis", "Type", "Language", "Size", "Content", "Content"],
            [emojis, post_type, language, size, post_content, post_improvements],
        ):
            if field in POST_VALIDATIONS and POST_VALIDATIONS[field][0](value):
                self.error_handling(POST_VALIDATIONS[field][1])
                return

        if self.selected_post_index is None:
            suggestion = self.general_adjust_assistant.send_request(
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
        post.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
        post.setWordWrap(True)
        post.setContentsMargins(5, 10, 5, 20)
        post_container = QHBoxLayout()
        post_container.addWidget(post)
        self.improved_posts_layout.addLayout(post_container)

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
        raise KeyError("Post not found")

    def open_stored_posts(self):
        self.stored_posts = StoredPosts(self.suggestions)
        self.stored_posts.selectPost.connect(self.set_selected_post)
        self.stored_posts.show()

    def set_selected_post(self, post):
        clear_layout(self.improved_posts_layout)
        self.selected_post_index = self.suggestions.index(post)
        self.post_content_edit.setText(post)


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
        self.post_content_edit = QTextEdit()
        self.post_content_edit.setLineWrapMode(QTextEdit.LineWrapMode.WidgetWidth)
        input_layout.addWidget(self.post_content_edit)

        self.translate_post_button = QPushButton("Translate Post")
        self.translate_post_button.clicked.connect(self.translate_post)
        form_options_layout = QHBoxLayout()
        form_options_layout.addStretch()
        form_options_layout.addWidget(self.translate_post_button)
        input_layout.addLayout(form_options_layout)

        output_layout = QVBoxLayout()

        title_label = QLabel("Translated post:")
        title_label.setContentsMargins(0, 4, 0, 4)
        output_layout.addWidget(title_label)
        self.post_translated_label = QLabel()
        self.post_translated_label.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding
        )
        self.post_translated_label.setStyleSheet("border: 1px solid #CACACA;")
        self.post_translated_label.setTextInteractionFlags(
            Qt.TextInteractionFlag.TextSelectableByMouse
        )
        self.post_translated_label.setWordWrap(True)
        self.post_translated_label.setContentsMargins(5, 10, 5, 20)
        output_layout.addWidget(self.post_translated_label)

        language_form_layout = QHBoxLayout()
        language_form_layout.addStretch()
        self.language_cb = QComboBox()
        self.language_cb.setMinimumWidth(200)
        self.language_cb.addItems(["English", "Potuguese", "Spanish"])
        language_form_layout.addWidget(self.language_cb)
        output_layout.addLayout(language_form_layout)

        main_layout.addLayout(input_layout)
        main_layout.addLayout(output_layout)

        self.setLayout(main_layout)

        self.suggestions = suggestions

    def translate_post(self):
        self.translate_post_button.setDisabled(True)

        post_content = self.post_content_edit.toPlainText()
        language = str(self.language_cb.currentText())

        for field, value in zip(["Language", "Content"], [language, post_content]):
            if field in POST_VALIDATIONS and POST_VALIDATIONS[field][0](value):
                self.error_handling(POST_VALIDATIONS[field][1])
                return

        self.translate_assistant.set_language(language)
        translation = self.translate_message(post_content)
        self.post_translated_label.setText(translation)

        self.translate_post_button.setDisabled(False)

    @pyqtSlot(str)
    def selected_post(self, post):
        self.post_content_edit.setText(post)

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


def clear_layout(main_layout):
    for i in reversed(range(main_layout.count())):
        item = main_layout.itemAt(i)
        widget = item.widget()
        if widget is not None:
            widget.setParent(None)
            main_layout.removeWidget(widget)
        else:
            clear_layout(item.layout())
