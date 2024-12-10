from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (QHBoxLayout, QLabel, QLineEdit, QPushButton,
                             QScrollArea, QVBoxLayout, QWidget)

from core.chat import Chat
from ui.base import ErrorHandling
from ui.utils import clear_layout


class ChatUI(QWidget, ErrorHandling):
    MESSAGE_SIZE_PERCENTAGE = 0.9

    message_labels = []
    chat = Chat()

    def __init__(self):
        super().__init__()
        main_layout = QVBoxLayout()

        options_layout = QHBoxLayout()
        options_layout.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.clear_button = QPushButton("Clear")
        self.clear_button.clicked.connect(self.clear_chat)
        options_layout.addWidget(self.clear_button)
        main_layout.addLayout(options_layout)

        self.messages_layout = QVBoxLayout()
        self.messages_container = QWidget()
        self.messages_container.setLayout(self.messages_layout)
        messages_scroll = QScrollArea()
        messages_scroll.setWidget(self.messages_container)
        messages_scroll.setWidgetResizable(True)
        main_layout.addWidget(messages_scroll)

        input_layout = QHBoxLayout()
        self.message_edit = QLineEdit()
        input_layout.addWidget(self.message_edit)
        self.send_message_button = QPushButton("Send")
        self.send_message_button.clicked.connect(self.send_message)
        input_layout.addWidget(self.send_message_button)
        main_layout.addLayout(input_layout)

        self.setLayout(main_layout)

    def resizeEvent(self, a0):
        self.message_size = int(
            self.messages_container.width() * self.MESSAGE_SIZE_PERCENTAGE
        )

        for message_widget in self.message_labels:
            message_widget.setMinimumWidth(self.message_size)
            message_widget.setMaximumWidth(self.message_size)

        super().resizeEvent(a0)

    def send_message(self):
        self.send_message_button.setDisabled(True)
        message = self.message_edit.text()
        self.message_edit.clear()

        if len(message) <= 10:
            self.error_handling("Message content must be 10 characters or more")
            self.send_message_button.setDisabled(False)
            return

        self.message_size = int(
            self.messages_container.width() * self.MESSAGE_SIZE_PERCENTAGE
        )

        user_message_label = self.add_message_label(message)
        self.messages_layout.addWidget(user_message_label)

        response = self.chat.send_request(message)

        bot_response_label = self.add_message_label(response)

        bot_response_layout = QHBoxLayout()
        bot_response_layout.addWidget(bot_response_label)
        bot_response_layout.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.messages_layout.addLayout(bot_response_layout)

        self.send_message_button.setDisabled(False)

    def add_message_label(self, message):
        message_label = QLabel(message)
        message_label.setMinimumWidth(self.message_size)
        message_label.setMaximumWidth(self.message_size)
        message_label.setWordWrap(True)
        self.message_labels.append(message_label)
        return message_label

    def clear_chat(self):
        clear_layout(self.messages_layout)
        self.chat.reset_chat()
