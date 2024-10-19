import os

import dotenv
from openai import OpenAI

from Utils.patterns import singleton

dotenv.load_dotenv()


class Dalle:
    _client = None

    def __init__(self, model="dall-e-3", size="1024x1024", quality="standard"):
        self.model = model
        self.size = size
        self.quality = quality

    @property
    def client(self):
        if self._client is None:
            self._set_client()
        return self._client

    def _set_client(self):
        api_key = os.environ.get("OPENAI_KEY")
        self._client = OpenAIUnique(api_key=api_key)

    def send_request(self, prompt):
        response = self.client.images.generate(
            model=self.model,
            prompt=prompt,
            size=self.size,
            quality=self.quality,
            n=1,
        )

        return response.data[0].url


@singleton
class OpenAIUnique(OpenAI):
    pass


if __name__ == "__main__":
    instance = Dalle()

    print(
        instance.send_request(
            "Logo para empresa de Energia Solar com as inicias NMV (Novo Mundo Verde)"
        )
    )
