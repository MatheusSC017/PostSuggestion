import os

import dotenv

from Core.base import OpenAIUnique
from Utils.patterns import singleton

dotenv.load_dotenv()


@singleton
class Dalle:
    _client = None

    @property
    def client(self):
        if self._client is None:
            self._set_client()
        return self._client

    def _set_client(self):
        api_key = os.environ.get("OPENAI_KEY")
        self._client = OpenAIUnique(api_key=api_key)

    def generate_image(self, prompt, size="1024x1024", quality="standard"):
        if len(prompt) < 10:
            raise ValueError("Prompt text must contain at least 10 characters")

        if size not in ("256x256", "512x512", "1024x1024", "1792x1024", "1024x1792"):
            raise ValueError(
                'The size must be between the listed values: ["256x256", "512x512", "1024x1024", "1792x1024", "1024x1792"], '
                "if a value is not provided the generated image will be of the proportions 1024x1024"
            )
        if quality not in ("standard", "hd"):
            raise ValueError(
                'The quality must be between the listed values: ["standard", "hd"], if a value is not provided the generated '
                "image will be of the quality standard"
            )

        model = "dall-e-3" if size not in ("256x256", "512x512") else "dall-e-2"

        response = self.client.images.generate(
            model=model,
            prompt=prompt,
            size=size,
            quality=quality,
            n=1,
        )

        return response.data[0].url

    def update_image(self, prompt, image_byte, mask_byte, size="1024x1024"):
        if len(prompt) < 10:
            raise ValueError("Prompt text must contain at least 10 characters")

        if size not in ("256x256", "512x512", "1024x1024", "1792x1024", "1024x1792"):
            raise ValueError(
                'The size must be between the listed values: ["256x256", "512x512", "1024x1024", "1792x1024", "1024x1792"], '
                "if a value is not provided the generated image will be of the proportions 1024x1024"
            )

        response = self.client.images.edit(
            model="dall-e-2",
            image=image_byte,
            mask=mask_byte,
            prompt=prompt,
            n=1,
            size=size,
        )

        return response.data[0].url

    def generate_variations(self, prompt, image_byte, size="1024x1024"):
        if len(prompt) < 10:
            raise ValueError("Prompt text must contain at least 10 characters")

        if size not in ("256x256", "512x512", "1024x1024", "1792x1024", "1024x1792"):
            raise ValueError(
                'The size must be between the listed values: ["256x256", "512x512", "1024x1024", "1792x1024", "1024x1792"], '
                "if a value is not provided the generated image will be of the proportions 1024x1024"
            )

        response = self.client.images.create_variation(
            image=image_byte, n=2, model="dall-e-2", size=size
        )

        return response.data[0].url, response.data[1].url


if __name__ == "__main__":
    instance = Dalle()

    print(
        instance.generate_image(
            "Logo para empresa de Energia Solar com as inicias NMV (Novo Mundo Verde), Utilize somente a sigla como texto",
            "NMV",
            size="256x256",
        )
    )
