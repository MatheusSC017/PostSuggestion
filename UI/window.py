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
    QPushButton
)
from PyQt6.QtGui import QAction, QIntValidator
from Core.main import OpenAIAssistants
from dotenv import load_dotenv


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        load_dotenv()
        self.assistants = OpenAIAssistants()

        self.settings()
        self.init_ui()

    def settings(self):
        self.setWindowTitle("AI Assitants")
        self.setMinimumWidth(1000)
        self.setMinimumHeight(700)

    def init_ui(self):
        self.set_menu()

        self.central_widget = QWidget()
        self.set_suggest_post_ui()
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
        self.emojis.addItems(["Low", "Medium", "High"])
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

        generate_posts_button = QPushButton("Generate Posts")
        generate_posts_button.clicked.connect(self.generate_posts)
        form_options = QHBoxLayout()
        form_options.addStretch()
        form_options.addWidget(generate_posts_button)
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
        # emojis = str(self.emojis.currentText())
        # post_type = str(self.type.currentText())
        # language = str(self.language.currentText())
        # size = int(self.size.text())
        post_content = self.post_content.toPlainText()

        suggestions = self.assistants.get_suggestion(product_characteristics=post_content)
        for suggestion in suggestions:
            post = QLabel(suggestion)
            post.setWordWrap(True)
            post.setContentsMargins(5, 10, 5, 20)
            self.generated_posts.addWidget(post)

    def set_improve_post_ui(self):
        pass

    def set_translate_post_ui(self):
        pass


if __name__ == "__main__":
    app = QApplication([])
    main = MainWindow()
    main.show()
    app.exec()
