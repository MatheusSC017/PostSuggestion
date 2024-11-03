import json

from Core.base import ChatGPT


class TranslatorAssistant(ChatGPT):
    def __init__(self, language="English", *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.language = language
        self.messages[0][
            "content"
        ] = "You are a useful assistant who translates post into specified language"

    def set_language(self, language):
        self.language = language

    def send_request(self, message):
        self.messages.append(
            {
                "role": "user",
                "content": f"Language: {self.language}\nMessage: {message}",
            }
        )
        response = self.client.chat.completions.create(
            model=self.model,
            messages=self.messages,
            temperature=0,
        )
        response = json.loads(response.model_dump_json())["choices"][0]["message"][
            "content"
        ]

        self.messages.append({"role": "assistant", "content": response})
        return response
