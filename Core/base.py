from openai import OpenAI
from abc import ABC, abstractmethod
import dotenv
import pathlib
import os
import copy
import json

from Utils.patterns import singleton
from Utils.types import Configs

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

        self.messages = [{
            "role": "system",
            "content": ""
        }, ]

    @property
    def client(self):
        if self._client is None:
            self._set_client()
        return self._client

    def _set_client(self):
        api_key = os.environ.get('OPENAI_KEY')
        self._client = OpenAIUnique(api_key=api_key)

    @abstractmethod
    def send_request(self, message):
        user_request = copy.deepcopy(self.basic_configs)
        user_request['Characteristics'] = message
        self.messages.append({
            "role": "user",
            "content": "Rules: \n\n" + '\n'.join([': '.join((getattr(Configs, k.upper(), k), str(v)))
                                                  for k, v in user_request.items()])
        })
        response = self.client.chat.completions.create(
            model=self.model,
            messages=self.messages,
            temperature=0,
        )
        response = json.loads(response.model_dump_json())["choices"][0]["message"]["content"]

        self.messages.append({"role": "assistant", "content": response})
        return response


@singleton
class OpenAIUnique(OpenAI):
    pass
