import os
import pathlib
from abc import ABC, abstractmethod

import dotenv
from openai import OpenAI
from PyQt6.QtWidgets import QMessageBox

from utils.patterns import singleton

BASEDIR = pathlib.Path().resolve()
dotenv.load_dotenv(BASEDIR / ".env")


class ChatGPT(ABC):
    model = ""
    _client = None
    responses = []
    messages = []
    basic_configs = {}

    def __init__(self, model="gpt-3.5-turbo", basic_configs={}):
        self.model = model

        for key, value in basic_configs.items():
            self.basic_configs[key] = value

        self.messages = [
            {"role": "system", "content": ""},
        ]

    @property
    def client(self):
        if self._client is None:
            self._set_client()
        return self._client

    def _set_client(self):
        api_key = os.environ.get("OPENAI_KEY")
        self._client = OpenAIUnique(api_key=api_key)

    @abstractmethod
    def send_request(self, message):
        pass


@singleton
class OpenAIUnique(OpenAI):
    pass


class ErrorHandling:
    def error_handling(self, message):
        dlg = QMessageBox(self)
        dlg.setWindowTitle("Error")
        dlg.setText(message)
        dlg.exec()
