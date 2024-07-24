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


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.assistants = OpenAIAssistants()

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
        self.size.setValidator(QIntValidator(2, 99))
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
        input_layout.addWidget(self.post_content)

        generate_posts = QPushButton("Generate Posts")
        form_options = QHBoxLayout()
        form_options.addStretch()
        form_options.addWidget(generate_posts)
        input_layout.addLayout(form_options)

        output_layout = QVBoxLayout()

        output_layout.addWidget(QLabel("Suggeestions"))
        self.generated_posts = QVBoxLayout()
        post1 = QLabel("Lorem ipsum sollicitudin suspendisse proin scelerisque nibh porta lorem scelerisque porta ultrices, varius euismod nec vel per venenatis adipiscing non sollicitudin eros convallis, dictumst eu interdum a id est mollis ullamcorper sagittis congue. fusce nec donec purus luctus dapibus sit lobortis aliquam justo, fringilla luctus interdum varius erat pretium donec commodo tortor, nunc ac torquent in iaculis at accumsan nam. in tempor nulla mauris mi habitasse hendrerit mollis blandit vel etiam mauris, ullamcorper metus sociosqu felis nullam cubilia et vulputate leo tincidunt quam, duis habitant hendrerit tempus integer congue faucibus pulvinar quis semper.")
        post1.setWordWrap(True)
        post1.setContentsMargins(5, 10, 5, 20)
        post2 = QLabel("Erat nullam elit donec hac elit risus per class hendrerit non, rutrum cursus inceptos senectus viverra aenean nisi dolor vel, nunc lectus suscipit pretium tempor velit vel nisl pharetra. convallis dapibus est cras molestie scelerisque habitant sagittis, aenean accumsan eu condimentum fermentum viverra tempor, fermentum vel integer torquent nulla fermentum. aptent id habitant potenti quisque neque elementum curabitur velit, congue curae pretium curabitur lacinia urna egestas, luctus blandit malesuada aenean eros quis donec. varius eu congue lacus leo eros metus ac nulla sagittis, lobortis molestie quisque elit vel lacus aliquam sapien aptent, aliquet aliquam leo tempus aliquam dui ut mollis.")
        post2.setWordWrap(True)
        post2.setContentsMargins(5, 10, 5, 20)
        post3 = QLabel("Cubilia in ac venenatis placerat felis id risus pretium duis, mattis tempus lectus pretium consequat auctor class consequat inceptos imperdiet, gravida placerat mollis sem sed enim nulla quam. nec tristique nunc in rhoncus nibh suscipit magna felis, luctus commodo nibh fusce quis interdum class magna euismod, vulputate donec taciti sit urna massa cubilia. pellentesque malesuada himenaeos sodales dapibus platea id urna cubilia netus, ut et aliquet nisl aenean sed litora quisque imperdiet cursus, nunc taciti aliquet vel ultrices ad dui eros. imperdiet sit a ornare morbi fermentum luctus nibh duis egestas amet posuere vivamus, dictum curabitur vivamus interdum dapibus felis suspendisse risus duis malesuada felis praesent proin, massa vehicula aptent platea nec primis feugiat semper duis eros bibendum.")
        post3.setWordWrap(True)
        post3.setContentsMargins(5, 10, 5, 20)
        post4 = QLabel("Cubilia in ac venenatis placerat felis id risus pretium duis, mattis tempus lectus pretium consequat auctor class consequat inceptos imperdiet, gravida placerat mollis sem sed enim nulla quam. nec tristique nunc in rhoncus nibh suscipit magna felis, luctus commodo nibh fusce quis interdum class magna euismod, vulputate donec taciti sit urna massa cubilia. pellentesque malesuada himenaeos sodales dapibus platea id urna cubilia netus, ut et aliquet nisl aenean sed litora quisque imperdiet cursus, nunc taciti aliquet vel ultrices ad dui eros. imperdiet sit a ornare morbi fermentum luctus nibh duis egestas amet posuere vivamus, dictum curabitur vivamus interdum dapibus felis suspendisse risus duis malesuada felis praesent proin, massa vehicula aptent platea nec primis feugiat semper duis eros bibendum.")
        post4.setWordWrap(True)
        post4.setContentsMargins(5, 10, 5, 20)
        self.generated_posts.addWidget(post1)
        self.generated_posts.addWidget(post2)
        self.generated_posts.addWidget(post3)
        self.generated_posts.addWidget(post4)
        container = QWidget()
        container.setLayout(self.generated_posts)
        scroll_posts = QScrollArea()
        scroll_posts.setWidget(container)
        scroll_posts.setWidgetResizable(True)
        output_layout.addWidget(scroll_posts)

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
