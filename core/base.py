from openai import OpenAI
import copy
import json
from abc import ABC, abstractmethod
import re

from core.adjustment import AdjustmentPost


class ChatGPT(ABC):
    model = ""
    client = None
    responses = []
    messages = []
    basic_configs = {}

    def __init__(self, api_key, model="gpt-3.5-turbo", basic_configs={}):
        self.model = model
        self.client = OpenAI(api_key=api_key)

        for key, value in basic_configs.items():
            self.basic_configs[key] = value

        self.messages.append([{
            "role": "system",
            "content": ""
        }, ])

    @abstractmethod
    def send_request(self):
        pass
