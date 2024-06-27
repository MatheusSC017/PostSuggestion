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
    QScrollArea
)
from PyQt6.QtGui import QAction


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.settings()
        self.init_ui()

    def settings(self):
        self.setWindowTitle("AI Assitants")
        self.setMinimumWidth(1000)
        self.setMinimumHeight(700)

    def init_ui(self):
        self.set_menu()

        main_layout = self.set_suggest_post_ui()

        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

    def set_menu(self):
        menu_bar = QMenuBar(self)
        self.setMenuBar(menu_bar)

        post_assistants = QMenu("Posts", self)

        self.suggest_post_menu = QAction("Suggestion")
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
        emojis = QComboBox()
        emojis.addItems(["Low", "Medium", "High"])
        column_options_1.addWidget(emojis)
        column_options_1.addWidget(QLabel("Type"))
        type = QComboBox()
        type.addItems(["Product", "Service", "Event", "Others"])
        column_options_1.addWidget(type)

        column_options_2 = QVBoxLayout()
        column_options_2.addWidget(QLabel("Size"))
        column_options_2.addWidget(QLineEdit())
        column_options_2.addWidget(QLabel("Language"))
        language = QComboBox()
        language.addItems(["English", "Potuguese", "Spanish"])
        column_options_2.addWidget(language)

        options = QHBoxLayout()
        options.addLayout(column_options_1)
        options.addLayout(column_options_2)

        input_layout.addLayout(options)
        input_layout.addWidget(QLabel("Type your request:"))
        input_layout.addWidget(QTextEdit())

        output_layout = QVBoxLayout()

        output_layout.addWidget(QLabel("Suggeestions"))
        output_layout.addWidget(QScrollArea())

        main_layout.addLayout(input_layout)
        main_layout.addLayout(output_layout)

        return main_layout

    def set_improve_post_ui(self):
        pass

    def set_translate_post_ui(self):
        pass


if __name__ == "__main__":
    app = QApplication([])
    main = MainWindow()
    main.show()
    app.exec()
