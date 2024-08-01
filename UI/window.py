from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QHBoxLayout,
    QVBoxLayout,
    QMenuBar,
    QMenu,
    QWidget,
    QLabel,
    QTextEdit,
    QLineEdit,
    QComboBox,
    QScrollArea,
    QPushButton,
    QMessageBox
)
from PyQt6.QtGui import QAction, QIntValidator
from Core.main import OpenAIAssistants
from Core.adjustment import AdjustmentPostAssitantWithoutHistory
from dotenv import load_dotenv
from Utils.types import Emojis


class MainWindow(QMainWindow):

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

        self.central_widget = QWidget()
        self.set_translate_post_ui()

        self.setCentralWidget(self.central_widget)

    def set_menu(self):
        menu_bar = QMenuBar(self)
        self.setMenuBar(menu_bar)

        post_assistants = QMenu("Posts", self)

        self.suggest_post_menu = QAction("Suggestion")
        self.suggest_post_menu.triggered.connect(self.set_suggest_post_ui)
        self.improve_post_menu = QAction("Improvement")
        self.translate_post_menu = QAction("Translate")
        post_assistants.addAction(self.suggest_post_menu)
        post_assistants.addAction(self.improve_post_menu)
        post_assistants.addAction(self.translate_post_menu)

        menu_bar.addMenu(post_assistants)

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

        main_layout.addLayout(input_layout)
        main_layout.addLayout(output_layout)

        self.central_widget.setLayout(main_layout)

    def generate_posts(self):
        self.generate_posts_button.setDisabled(True)
        emojis = getattr(Emojis, str(self.emojis.currentText()).upper())
        post_type = str(self.type.currentText())
        language = str(self.language.currentText())
        size = int(self.size.text())
        post_content = self.post_content.toPlainText()

        if len(post_content) <= 30:
            dlg = QMessageBox(self)
            dlg.setWindowTitle("Error")
            dlg.setText("Post content must be 30 characters or more")
            dlg.exec()
            return

        if 100 > size > 5000:
            dlg = QMessageBox(self)
            dlg.setWindowTitle("Error")
            dlg.setText("The generated post size must be between 100 and 5000")
            dlg.exec()
            return

        suggestions = self.assistants.get_suggestion(
            product_characteristics=post_content,
            Emojis=emojis,
            Type=post_type,
            Language=language,
            Size=size
        )
        for suggestion in suggestions:
            post = QLabel(suggestion)
            post.setWordWrap(True)
            post.setContentsMargins(5, 10, 5, 20)
            post_container = QHBoxLayout()
            post_container.addWidget(post)
            self.generated_posts.addLayout(post_container)
        self.generate_posts_button.setDisabled(False)

    def set_improve_post_ui(self):
        main_layout = QHBoxLayout()

        input_layout = QVBoxLayout()

        input_layout.addWidget(QLabel("Post:"))
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

        self.central_widget.setLayout(main_layout)

    def improve_post(self):
        self.improve_post_button.setDisabled(True)

        post_content = self.post_content.toPlainText()
        post_improvements = self.post_improvements.toPlainText()

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

        suggestion = self.adjust_assistant.adjust_post(post_content, post_improvements)
        post = QLabel(suggestion)
        post.setWordWrap(True)
        post.setContentsMargins(5, 10, 5, 20)
        post_container = QHBoxLayout()
        post_container.addWidget(post)
        self.improved_posts.addLayout(post_container)

        self.improve_post_button.setDisabled(False)

    def set_translate_post_ui(self):
        main_layout = QHBoxLayout()

        input_layout = QVBoxLayout()

        input_layout.addWidget(QLabel("Post:"))
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

        self.central_widget.setLayout(main_layout)

    def translate_post(self):
        self.translate_post_button.setDisabled(True)

        post_content = self.post_content.toPlainText()

        if len(post_content) <= 30:
            dlg = QMessageBox(self)
            dlg.setWindowTitle("Error")
            dlg.setText("Post content must be 30 characters or more")
            dlg.exec()
            return

        self.assistants.translate_assistant.set_language(str(self.language.currentText()))
        translation = self.assistants.translate_message(post_content)
        self.post_translated.setText(translation)

        self.translate_post_button.setDisabled(False)


if __name__ == "__main__":
    app = QApplication([])
    main = MainWindow()
    main.show()
    app.exec()
